import os
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.auth.models import RoleModel, UserModels
from app.auth.schemas import UserRegisterSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
STUDENT_ROLE_NAME = "Студент"


class RoleService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def list_roles(self) -> list[RoleModel]:
        result = await self.db.execute(select(RoleModel).order_by(RoleModel.id))
        return list(result.scalars().all())

    async def get_by_name(self, name: str) -> RoleModel | None:
        result = await self.db.execute(select(RoleModel).where(RoleModel.name == name))
        return result.scalars().first()

    async def get_required_by_name(self, name: str) -> RoleModel:
        role = await self.get_by_name(name)
        if role is None:
            raise ValueError(f"Role '{name}' is not initialized")
        return role

    async def create_if_not_exists(self, name: str) -> RoleModel:
        role = await self.get_by_name(name)
        if role:
            return role

        role = RoleModel(name=name)
        self.db.add(role)
        await self.db.flush()
        return role


class AuthService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.secret_key = os.getenv("JWT_SECRET_KEY")
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, user_id: int, expires_delta: int = 60) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_delta),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    async def get_user_by_login(self, login: str) -> UserModels | None:
        result = await self.db.execute(
            select(UserModels)
            .where(UserModels.login == login)
            .options(joinedload(UserModels.role))
        )
        return result.scalars().first()

    async def create_user(self, user_data: UserRegisterSchema) -> UserModels:
        role = await RoleService(self.db).get_required_by_name(STUDENT_ROLE_NAME)

        new_user = UserModels(
            login=user_data.login,
            fio=user_data.fio,
            hashed_password=self.hash_password(user_data.password),
            role_id=role.id,
        )

        self.db.add(new_user)
        await self.db.commit()

        created_user = await self.get_user_by_login(new_user.login)
        if created_user is None:
            raise RuntimeError("Created user was not found")

        return created_user
