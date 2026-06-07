from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.services import RoleService, STUDENT_ROLE_NAME

DEFAULT_ROLE_NAMES = (STUDENT_ROLE_NAME, "Преподаватель", "Администратор")


async def seed_roles(db: AsyncSession) -> None:
    role_service = RoleService(db)

    for role_name in DEFAULT_ROLE_NAMES:
        await role_service.create_if_not_exists(role_name)

    await db.commit()
