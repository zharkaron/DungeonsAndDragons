import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://dnd_user:dnd_password@postgres:5432/dnd"
)

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")
)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
