from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")


@router.get("/health")
async def healthcheck():
    return {"status": "ok"}
