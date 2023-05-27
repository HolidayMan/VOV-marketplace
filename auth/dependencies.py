from typing import Annotated

from fastapi import Cookie, Depends
from .logic import get_user_by_token
from .models import UserInDB
from .repository import FAKE_REPO


def get_token_cookie(access_token: Annotated[str | None, Cookie()] = None) -> str | None:
    return access_token


def get_current_user(token: str | None = Depends(get_token_cookie)) -> UserInDB | None:
    if not token:
        return None
    return get_user_by_token(FAKE_REPO, token)
