import asyncio

from app.auth.seed import seed_roles
from app.database import async_session


async def run_seed() -> None:
    async with async_session() as db:
        await seed_roles(db)


if __name__ == "__main__":
    asyncio.run(run_seed())
