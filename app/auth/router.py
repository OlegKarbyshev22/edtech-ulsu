from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth.schemas import UserRegisterSchema, UserLoginSchema, UserResponseSchema, TokenSchema
from app.auth.services import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegisterSchema, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    
    existing_user = await auth_service.get_user_by_login(user_data.login)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Пользователь с таким логином уже существует"
        )
    
    new_user = await auth_service.create_user(user_data)
    return new_user

@router.post("/login", response_model=TokenSchema)
async def login(user_data: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    
    user = await auth_service.get_user_by_login(user_data.login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Неверный логин или пароль"
        )
    
    if not auth_service.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Неверный логин или пароль"
        )
    
    token = auth_service.create_access_token(user_id=user.id)
    return {"access_token": token, "token_type": "bearer"}