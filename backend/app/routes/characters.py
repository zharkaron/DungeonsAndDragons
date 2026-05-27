from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.character import Character
from app.models.user import User
from app.schemas.character import (
    CharacterCreate,
    CharacterResponse,
    CharacterUpdate,
)
from app.services.character_permission import (
    check_campaign_membership,
    check_character_permission,
)

router = APIRouter(prefix="/characters", tags=["Characters"])


@router.post(
    "",
    response_model=CharacterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_character(
    body: CharacterCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new character. User must be a member of the campaign."""
    await check_campaign_membership(db, body.campaign_id, current_user.id)

    character = Character(
        name=body.name,
        race=body.race,
        character_class=body.character_class,
        level=body.level,
        hp=body.hp,
        ac=body.ac,
        speed=body.speed,
        strength=body.strength,
        dexterity=body.dexterity,
        constitution=body.constitution,
        intelligence=body.intelligence,
        wisdom=body.wisdom,
        charisma=body.charisma,
        hit_dice=body.hit_dice,
        user_id=current_user.id,
        campaign_id=body.campaign_id,
    )

    db.add(character)
    await db.commit()
    await db.refresh(character)

    return character


@router.get(
    "",
    response_model=List[CharacterResponse],
)
async def get_my_characters(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all characters owned by the authenticated user."""
    result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    characters = result.scalars().all()
    return characters


@router.get(
    "/{character_id}",
    response_model=CharacterResponse,
)
async def get_character(
    character_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific character. Users can view their own; DMs can view any in their campaigns."""
    character = await check_character_permission(
        db, character_id, current_user.id, can_update=False
    )
    return character


@router.put("/{character_id}", response_model=CharacterResponse)
async def update_character(
    character_id: int,
    body: CharacterUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a character. Owners and DMs of the campaign can edit."""
    character = await check_character_permission(
        db, character_id, current_user.id
    )

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(character, field, value)

    await db.commit()
    await db.refresh(character)

    return character


@router.patch("/{character_id}", response_model=CharacterResponse)
async def patch_character(
    character_id: int,
    body: CharacterUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Partially update a character. Owners and DMs of the campaign can edit."""
    character = await check_character_permission(
        db, character_id, current_user.id
    )

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(character, field, value)

    await db.commit()
    await db.refresh(character)

    return character


@router.delete("/{character_id}")
async def delete_character(
    character_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a character. Only the owner or DM can delete."""
    character = await check_character_permission(
        db, character_id, current_user.id
    )

    await db.delete(character)
    await db.commit()

    return {"detail": "Character deleted successfully"}