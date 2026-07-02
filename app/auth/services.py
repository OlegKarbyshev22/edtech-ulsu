import os
import hashlib
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.auth.models import Role, User
from app.auth.schemas import UserRegisterSchema

BCRYPT_SHA256_PREFIX = "bcrypt_sha256$"
STUDENT_ROLE_NAME = "Студент"


def _password_digest(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).hexdigest().encode("ascii")


class RoleService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def list_roles(self) -> list[Role]:
        result = await self.db.execute(select(Role).order_by(Role.id))
        return list(result.scalars().all())

    async def get_by_name(self, name: str) -> Role | None:
        result = await self.db.execute(select(Role).where(Role.name == name))
        return result.scalars().first()

    async def get_required_by_name(self, name: str) -> Role:
        role = await self.get_by_name(name)
        if role is None:
            raise ValueError(f"Role '{name}' is not initialized")
        return role

    async def create_if_not_exists(self, name: str) -> Role:
        role = await self.get_by_name(name)
        if role:
            return role

        role = Role(name=name)
        self.db.add(role)
        await self.db.flush()
        return role


class AuthService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.secret_key = os.getenv("JWT_SECRET_KEY")
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    def hash_password(self, password: str) -> str:
        hashed = bcrypt.hashpw(_password_digest(password), bcrypt.gensalt())
        return BCRYPT_SHA256_PREFIX + hashed.decode("ascii")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            if hashed_password.startswith(BCRYPT_SHA256_PREFIX):
                stored_hash = hashed_password.removeprefix(BCRYPT_SHA256_PREFIX)
                return bcrypt.checkpw(
                    _password_digest(plain_password),
                    stored_hash.encode("ascii"),
                )

            password_bytes = plain_password.encode("utf-8")
            if len(password_bytes) > 72:
                return False

            return bcrypt.checkpw(password_bytes, hashed_password.encode("ascii"))
        except (TypeError, ValueError):
            return False

    def create_access_token(self, user_id: int, expires_delta: int = 60) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_delta),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    async def get_user_by_login(self, login: str) -> User | None:
        result = await self.db.execute(
            select(User)
            .where(User.login == login)
            .options(joinedload(User.role))
        )
        return result.scalars().first()

    async def create_user(self, user_data: UserRegisterSchema) -> User:
        role = await RoleService(self.db).get_required_by_name(STUDENT_ROLE_NAME)

        new_user = User(
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
