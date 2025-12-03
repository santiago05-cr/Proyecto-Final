import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Intentar leer configuración de Clever Cloud
CLEVER_USER = os.getenv("CLEVER_USER")
CLEVER_PASSWORD = os.getenv("CLEVER_PASSWORD")
CLEVER_HOST = os.getenv("CLEVER_HOST")
CLEVER_PORT = os.getenv("CLEVER_PORT")
CLEVER_DATABASE = os.getenv("CLEVER_DATABASE")

# Si todas existen -> usar PostgreSQL
if all([CLEVER_USER, CLEVER_PASSWORD, CLEVER_HOST, CLEVER_PORT, CLEVER_DATABASE]):
    DATABASE_URL = (
        f"postgresql+asyncpg://{CLEVER_USER}:"
        f"{CLEVER_PASSWORD}@"
        f"{CLEVER_HOST}:"
        f"{CLEVER_PORT}/"
        f"{CLEVER_DATABASE}"
    )
else:
    # Modo TEST / fallback
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"   # base en RAM para pytest

# Crear engine
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session
