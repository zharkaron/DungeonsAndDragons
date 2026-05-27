from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime


class CampaignCreate(BaseModel):
    name: str
    description: str = ""

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Campaign name cannot be empty")
        return v


class CampaignJoinRequest(BaseModel):
    invite_code: str


class CampaignMemberResponse(BaseModel):
    id: int
    campaign_id: int
    user_id: int
    username: str
    role: str
    joined_at: datetime

    model_config = {"from_attributes": True}


class CampaignListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    invite_code: str

    model_config = {"from_attributes": True}


class CampaignResponse(BaseModel):
    id: int
    name: str
    description: str
    dm_id: int
    invite_code: str
    created_at: datetime
    members: List[CampaignMemberResponse] = []

    model_config = {"from_attributes": True}
