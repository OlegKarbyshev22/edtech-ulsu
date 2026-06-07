import asyncio

from app.auth.seed import seed_roles
from app.database import Base, async_session, engine

# Import models so SQLAlchemy registers them in Base.metadata.
from app.auth import models as auth_models  # noqa: F401
from app.thesis import models as thesis_models  # noqa: F401


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        await seed_roles(db)


if __name__ == "__main__":
    asyncio.run(init_db())
