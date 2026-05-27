from enum import Enum as PyEnum
from datetime import datetime
from typing import List

from sqlalchemy import String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, PyEnum):
    player = "player"
    dungeon_master = "dungeon_master"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="userrole", create_constraint=True),
        default=UserRole.player,
        server_default="player",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    campaigns: Mapped[List["Campaign"]] = relationship(
        back_populates="dm", foreign_keys="Campaign.dm_id"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"
