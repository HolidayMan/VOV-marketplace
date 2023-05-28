from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException, Form, Query
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from urllib.parse import quote_plus, unquote_plus

from domain.user import UserRole, User
from utils.templates import render
from .exceptions import CredentialsInvalid, UserAlreadyExists

from .services import process_user_login, process_create_user
from app import app
from .dependencies import get_current_user, get_uow


router = APIRouter(prefix="/auth")


@router.get("/logout", name="logout")
async def logout(next_: str = Query(default=None, alias="next"), user=Depends(get_current_user)):
    user_role = user.role if user else UserRole.CUSTOMER
    if next_:
        response = RedirectResponse(url=unquote_plus(next_), status_code=303)
    else:
        response = RedirectResponse(url=f"{router.url_path_for('login')}?role={user_role.value}", status_code=303)
    response.delete_cookie(key="access_token")
    return response


@router.get("/login", name="login")
async def login_form(request: Request, role: UserRole = UserRole.CUSTOMER, error: str = None,
                     user=Depends(get_current_user), next_: str = Query(default=None, alias="next")):
    if not next_:
        next_ = app.url_path_for('catalog')
    if user:
        return render(request, "auth/logout.html", {"next": quote_plus(str(request.url))})
    return render(request, "auth/login_form.html", {"role": role, "error": error, "next": quote_plus(next_)})


@router.post("/process-login", name="process_login")
async def process_login(email: Annotated[EmailStr, Form()],
                        password: Annotated[str, Form()], role: Annotated[UserRole, Form()],
                        next_: str = Query(default=None, alias="next"), uow=Depends(get_uow),
                        user=Depends(get_current_user)):
    if not next_:
        next_ = app.url_path_for('catalog')
    if user:
        return RedirectResponse(url=f"{router.url_path_for('login')}?role={role.value}"
                                    f"&next={quote_plus(next_)}", status_code=303)
    try:
        data = await process_user_login(uow, email, password, role)
    except CredentialsInvalid:
        return RedirectResponse(url=f"{router.url_path_for('login')}?error=Invalid credentials&role={role.value}"
                                    f"&next={quote_plus(next_)}",
                                status_code=303)
    response = RedirectResponse(url=f"{unquote_plus(next_)}", status_code=303)
    response.set_cookie(key="access_token", value=data["access_token"])
    return response


@router.get("/register", name="register")
async def register_form(request: Request, role: UserRole = UserRole.CUSTOMER,
                        error: str = None, user=Depends(get_current_user),
                        next_: str = Query(default=None, alias="next")):
    if not next_:
        next_ = app.url_path_for('catalog')
    if user:
        return render(request, "auth/logout.html", {"next": quote_plus(str(request.url))})
    return render(request, "auth/register_form.html", {"role": role, "error": error, "next": quote_plus(next_)})


@router.post("/process-register", name="process_register")
async def process_register(name: Annotated[str, Form()], email: Annotated[EmailStr, Form()],
                           password: Annotated[str, Form()], role: Annotated[UserRole, Form()],
                           next_: str = Query(default=None, alias="next"), uow=Depends(get_uow),
                           user=Depends(get_current_user)):
    if not next_:
        next_ = app.url_path_for('catalog')
    if user:
        return RedirectResponse(url=f"{router.url_path_for('register')}?&role={role.value}&next={quote_plus(next_)}",
                                status_code=303)
    error_message = "User with this email and role already exists"
    try:
        data = await process_create_user(uow, User(name=name, email=email, role=role), password)
    except UserAlreadyExists:
        return RedirectResponse(url=f"{router.url_path_for('register')}?error={error_message}&role={role.value}"
                                    f"&next={quote_plus(next_)}",
                                status_code=303)

    response = RedirectResponse(url=f"{unquote_plus(next_)}", status_code=303)
    response.set_cookie(key="access_token", value=data["access_token"])
    return response
