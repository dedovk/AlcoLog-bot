from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from AlcoLog.database.models import Base
from AlcoLog.utils.config import settings

DATABASE_URL = settings.DATABASE_URL

# Fix URL prefix if needed
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+asyncpg://", 1)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


async def close_db():
    await engine.dispose()
