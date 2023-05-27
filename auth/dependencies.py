from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status

from domain.user import UserRole
from .logic import get_user_by_token
from .models import UserInDB
from .repository import FAKE_REPO


def get_token_cookie(access_token: Annotated[str | None, Cookie()] = None) -> str | None:
    return access_token


def get_current_user(token: str | None = Depends(get_token_cookie)) -> UserInDB | None:
    if not token:
        return None
    return get_user_by_token(FAKE_REPO, token)


def get_user_role(user: UserInDB | None = Depends(get_current_user)) -> UserRole:
    if not user:
        return "customer"
    return user.role


def verify_customer(user_role: UserRole = Depends(get_user_role)) -> bool:
    return user_role == UserRole.CUSTOMER


def verify_seller(user_role: UserRole = Depends(get_user_role)) -> bool:
    return user_role == UserRole.SELLER


def verify_moderator(user_role: UserRole = Depends(get_user_role)) -> bool:
    return user_role == UserRole.MODERATOR


def require_auth(user: UserInDB | None = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


def require_role(role: UserRole):
    def wrapper(user_role: UserRole = Depends(get_user_role)):
        if user_role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return wrapper
