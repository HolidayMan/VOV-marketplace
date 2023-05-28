from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status

from domain.user import UserRole
from .logic import get_user_by_token
from .models import UserInDB
from .unit_of_work import MySQLAsyncUserUnitOfWork


def get_uow() -> MySQLAsyncUserUnitOfWork:
    return MySQLAsyncUserUnitOfWork()


def get_token_cookie(access_token: Annotated[str | None, Cookie()] = None) -> str | None:
    return access_token


async def get_current_user(token: str | None = Depends(get_token_cookie),
                           uow: MySQLAsyncUserUnitOfWork = Depends(get_uow)) -> UserInDB | None:
    if not token:
        return None
    return await get_user_by_token(uow, token)


async def get_user_role(user: UserInDB | None = Depends(get_current_user)) -> UserRole:
    if not user:
        return UserRole.CUSTOMER
    return user.role


async def verify_customer(user_role: UserRole = Depends(get_user_role)) -> bool:
    return user_role == UserRole.CUSTOMER


async def verify_seller(user_role: UserRole = Depends(get_user_role)) -> bool:
    return user_role == UserRole.SELLER


async def verify_moderator(user_role: UserRole = Depends(get_user_role)) -> bool:
    return user_role == UserRole.MODERATOR


async def require_auth(user: UserInDB | None = Depends(get_current_user)) -> UserInDB:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user


def require_role(role: UserRole):
    async def wrapper(user: UserInDB = Depends(get_current_user)) -> UserInDB:
        if user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user
    return wrapper
