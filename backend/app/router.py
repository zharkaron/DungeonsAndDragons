from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import check_db_connection, get_db

router = APIRouter(prefix="/api/v1")


@router.get("/health")
async def healthcheck():
    return {"status": "ok"}


@router.get("/db/health")
async def db_health():
    connected = await check_db_connection()
    status = "connected" if connected else "disconnected"
    return {"database": status}
