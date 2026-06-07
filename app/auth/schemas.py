from pydantic import BaseModel, Field


class RoleCreateSchema(BaseModel):
    name: str = Field(..., max_length=50, description="Название роли")


class RoleResponseSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserRegisterSchema(BaseModel):
    login: str = Field(..., min_length=3, max_length=100, description="Уникальный логин")
    password: str = Field(..., min_length=6, max_length=50, description="Пароль")
    fio: str = Field(..., min_length=5, max_length=100, description="ФИО пользователя")


class UserLoginSchema(BaseModel):
    login: str = Field(..., description="Логин пользователя")
    password: str = Field(..., description="Пароль")


class UserResponseSchema(BaseModel):
    id: int
    login: str
    fio: str
    role_id: int
    role: RoleResponseSchema

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
