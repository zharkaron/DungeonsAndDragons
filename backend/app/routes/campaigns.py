from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth import get_current_user
from app.database import get_db
from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.user import User, UserRole
from app.schemas.campaign import CampaignCreate, CampaignResponse
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
    )

    db.add(member)
    await db.commit()
    await db.refresh(member)

    members_response = [
        CampaignMemberResponse(
            id=member.id,
            campaign_id=member.campaign_id,
            user_id=member.user_id,
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
