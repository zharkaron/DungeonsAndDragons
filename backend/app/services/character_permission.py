from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.character import Character
from app.models.user import User


async def check_character_permission(
    db: AsyncSession,
    character_id: int,
    user_id: int,
    *,
    can_update: bool = True,
) -> Character:
    """Check that the user owns the character or is DM of the campaign.

    Returns the character.
    Raises 404 if character doesn't exist.
    Raises 403 if user isn't allowed to modify.
    """
    result = await db.execute(
        select(Character).where(Character.id == character_id)
    )
    character = result.scalar_one_or_none()
    if character is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found",
        )

    # Must be owner or DM of the campaign
    is_owner = character.user_id == user_id

    is_dm = False
    if not is_owner:
        campaign_result = await db.execute(
            select(Campaign).where(Campaign.id == character.campaign_id)
        )
        campaign_obj = campaign_result.scalar_one_or_none()
        if campaign_obj:
            is_dm = campaign_obj.dm_id == user_id

    if can_update and not is_owner and not is_dm:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this character",
        )
    elif not can_update and not is_owner and not is_dm:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this character",
        )

    return character


async def check_campaign_membership(
    db: AsyncSession,
    campaign_id: int,
    user_id: int,
) -> None:
    """Verify the user is a member of the campaign (required to create characters)."""
    result = await db.execute(
        select(CampaignMember).where(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == user_id,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be a member of this campaign to create characters",
        )