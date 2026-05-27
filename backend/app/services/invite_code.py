import secrets
import string

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign


def generate_invite_code() -> str:
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(6))


async def generate_unique_invite_code(db: AsyncSession) -> str:
    code = generate_invite_code()
    while True:
        result = await db.execute(select(Campaign).where(Campaign.invite_code == code))
        if not result.scalar_one_or_none():
            return code
        code = generate_invite_code()
