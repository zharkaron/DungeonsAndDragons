from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import check_db_connection, get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.routes.auth import router as auth_router
from app.routes.campaigns import router as campaigns_router
from app.routes.characters import router as characters_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(campaigns_router)
router.include_router(characters_router)


@router.get("/health")
async def healthcheck():
    return {"status": "ok"}


@router.get("/db/health")
async def db_health():
    connected = await check_db_connection()
    status = "connected" if connected else "disconnected"
    return {"database": status}


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """Protected endpoint that returns the current user profile."""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.value,
    }
