from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    race: Mapped[str] = mapped_column(String(50), nullable=False)
    character_class: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    hp: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    ac: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    speed: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    strength: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    dexterity: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    constitution: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    intelligence: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    wisdom: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    charisma: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    hit_dice: Mapped[str] = mapped_column(String(50), nullable=True, default="")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<Character(id={self.id}, name='{self.name}')>"