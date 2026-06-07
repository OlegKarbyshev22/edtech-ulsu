from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import UserLoginSchema, UserRegisterSchema
from app.auth.services import AuthService
from app.database import get_db

router = APIRouter(tags=["Auth pages"])
templates = Jinja2Templates(directory="templates")


def render_register(
    request: Request,
    error: str | None = None,
    form_data: dict | None = None,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "register.html",
        {"error": error, "form_data": form_data or {}},
    )


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return render_register(request)


@router.post("/register", response_class=HTMLResponse)
async def register_form(
    request: Request,
    fio: str = Form(...),
    login: str = Form(...),
    password: str = Form(...),
    password_repeat: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    form_data = {"fio": fio, "login": login}

    if password != password_repeat:
        return render_register(request, "Пароли не совпадают", form_data)

    auth_service = AuthService(db)
    if await auth_service.get_user_by_login(login):
        return render_register(request, "Пользователь с таким логином уже существует", form_data)

    try:
        user_data = UserRegisterSchema(fio=fio, login=login, password=password)
    except ValidationError as exc:
        message = exc.errors()[0]["msg"] if exc.errors() else "Проверьте данные формы"
        return render_register(request, message, form_data)

    try:
        await auth_service.create_user(user_data)
    except ValueError:
        return render_register(request, "Роль Студент не инициализирована. Выполните seed ролей.", form_data)

    return RedirectResponse("/login?registered=1", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, registered: int | None = None):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"registered": registered == 1, "error": None, "form_data": {}},
    )


@router.post("/login", response_class=HTMLResponse)
async def login_form(
    request: Request,
    login: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    form_data = {"login": login}
    user_data = UserLoginSchema(login=login, password=password)
    auth_service = AuthService(db)

    user = await auth_service.get_user_by_login(user_data.login)
    if not user or not auth_service.verify_password(user_data.password, user.hashed_password):
        return templates.TemplateResponse(
            request,
            "login.html",
            {"registered": False, "error": "Неверный логин или пароль", "form_data": form_data},
        )

    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=auth_service.create_access_token(user_id=user.id),
        httponly=True,
        samesite="lax",
    )
    return response
