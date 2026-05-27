from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth import get_current_user
from app.database import get_db
from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.user import User, UserRole
from app.schemas.campaign import (
    CampaignCreate,
    CampaignJoinRequest,
    CampaignMemberResponse,
    CampaignListResponse,
    CampaignResponse,
)
from app.services.invite_code import generate_unique_invite_code

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.post(
    "",
    response_model=CampaignResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_campaign(
    body: CampaignCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.dungeon_master:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Dungeon Masters can create campaigns",
        )

    invite_code = await generate_unique_invite_code(db)

    campaign = Campaign(
        name=body.name,
        description=body.description,
        dm_id=current_user.id,
        invite_code=invite_code,
    )

    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)

    member = CampaignMember(
        campaign_id=campaign.id,
        user_id=current_user.id,
        role="dm",
    )

    db.add(member)
    await db.commit()
    await db.refresh(member)

    members_response = [
        CampaignMemberResponse(
            id=member.id,
            campaign_id=member.campaign_id,
            user_id=member.user_id,
            username=current_user.username,
            role=member.role.value,
            joined_at=member.joined_at,
        )
    ]

    return CampaignResponse(
        id=campaign.id,
        name=campaign.name,
        description=campaign.description,
        dm_id=campaign.dm_id,
        invite_code=campaign.invite_code,
        created_at=campaign.created_at,
        members=members_response,
    )


@router.get(
    "/my",
    response_model=List[CampaignListResponse],
)
async def get_my_campaigns(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Campaign).where(
            Campaign.id.in_(
                select(CampaignMember.campaign_id).where(
                    CampaignMember.user_id == current_user.id
                )
            )
        )
    )
    campaigns = result.scalars().all()
    return campaigns


@router.get(
    "/{id}/members",
    response_model=List[CampaignMemberResponse],
)
async def get_campaign_members(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaign = await _get_campaign_or_404(db, id)

    is_dm = campaign.dm_id == current_user.id
    if not is_dm:
        await check_membership(db, campaign.id, current_user.id)

    result = await db.execute(
        select(CampaignMember, User).where(
            CampaignMember.campaign_id == id,
            CampaignMember.user_id == User.id,
        )
    )
    rows = result.all()

    members = [
        CampaignMemberResponse(
            id=member.id,
            campaign_id=member.campaign_id,
            user_id=member.user_id,
            username=user.username,
            role=member.role.value,
            joined_at=member.joined_at,
        )
        for member, user in rows
    ]
    return members


@router.delete("/{id}/members/{user_id}")
async def remove_member(
    id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaign = await _get_campaign_or_404(db, id)

    if campaign.dm_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the DM can remove members",
        )

    if campaign.dm_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove the DM from the campaign",
        )

    result = await db.execute(
        select(CampaignMember).where(
            CampaignMember.campaign_id == id,
            CampaignMember.user_id == user_id,
        )
    )
    member = result.scalar_one_or_none()
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )

    await db.delete(member)
    await db.commit()

    return {"detail": "Member removed successfully"}


@router.post("/{id}/join", response_model=CampaignMemberResponse)
async def join_campaign(
    id: int,
    body: CampaignJoinRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaign = await _get_campaign_or_404(db, id)

    if campaign.invite_code != body.invite_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid invite code",
        )

    existing = await db.execute(
        select(CampaignMember).where(
            CampaignMember.campaign_id == id,
            CampaignMember.user_id == current_user.id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are already a member of this campaign",
        )

    member = CampaignMember(
        campaign_id=campaign.id,
        user_id=current_user.id,
        role="player",
    )

    db.add(member)
    await db.commit()
    await db.refresh(member)

    return CampaignMemberResponse(
        id=member.id,
        campaign_id=member.campaign_id,
        user_id=member.user_id,
        role=member.role.value,
        joined_at=member.joined_at,
    )


async def _get_campaign_or_404(
    db: AsyncSession, campaign_id: int
) -> Campaign:
    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalar_one_or_none()
    if campaign is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )
    return campaign


async def check_membership(
    db: AsyncSession, campaign_id: int, user_id: int
):
    result = await db.execute(
        select(CampaignMember).where(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == user_id,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be a member of this campaign",
        )
