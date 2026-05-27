from datetime import datetime
from pydantic import BaseModel


class CharacterCreate(BaseModel):
    name: str
    race: str
    character_class: str
    level: int = 1
    hp: int = 10
    ac: int = 10
    speed: int = 30
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    hit_dice: str = ""
    campaign_id: int


class CharacterUpdate(BaseModel):
    name: str | None = None
    race: str | None = None
    character_class: str | None = None
    level: int | None = None
    hp: int | None = None
    ac: int | None = None
    speed: int | None = None
    strength: int | None = None
    dexterity: int | None = None
    constitution: int | None = None
    intelligence: int | None = None
    wisdom: int | None = None
    charisma: int | None = None
    hit_dice: str | None = None


class CharacterResponse(BaseModel):
    id: int
    name: str
    race: str
    character_class: str
    level: int
    hp: int
    ac: int
    speed: int
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    hit_dice: str
    user_id: int
    campaign_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}