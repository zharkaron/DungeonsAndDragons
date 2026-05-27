from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Integer, ForeignKey, DateTime, Enum as SAEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from sqlalchemy.sql import func


class CampaignMemberRole(str, PyEnum):
    dm = "dm"
    player = "player"


class CampaignMember(Base):
    __tablename__ = "campaign_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[CampaignMemberRole] = mapped_column(
        SAEnum(CampaignMemberRole, name="campaignmemberrole"),
        default=CampaignMemberRole.player,
        server_default="player",
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    campaign = relationship("Campaign", back_populates="members")
    user = relationship("User")
