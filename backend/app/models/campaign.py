from __future__ import annotations
from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from sqlalchemy.sql import func


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True, default="")
    dm_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    invite_code: Mapped[str] = mapped_column(
        String(10), unique=True, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    dm = relationship("User", back_populates="campaigns")
    members: Mapped[List["CampaignMember"]] = relationship(
        "CampaignMember", back_populates="campaign", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Campaign(id={self.id}, name='{self.name}')>"
