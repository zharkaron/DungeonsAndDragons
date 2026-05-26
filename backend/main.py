from fastapi import FastAPI
from app.router import router

app = FastAPI(title="D&D Campaign Manager")

app.include_router(router)
