from typing import Annotated

from fastapi import Header, Depends, HTTPException
from starlette import status

from domain.user import UserRole, User

# X-Token: asdlkjflkewjaw49jeioewjfjewija

def fake_get_user_with_custom_role(role: UserRole):
    def get_user(x_token: Annotated[str, Header()] = None) -> User | None:
        return User(
            id=1,
            name="admin",
            password_hash="asdlkjflkewjaw49jeioewjfjewija",
            user_role=role,
            email="example@example.com")
    return get_user


def fake_get_user(x_token: Annotated[str, Header()] = None) -> User | None:
    return User(
        id=1,
        name="admin",
        password_hash="asdlkjflkewjaw49jeioewjfjewija",
        user_role=UserRole.CUSTOMER,
        email="example@example.com"
    )


def fake_get_user_role(user: User = Depends(fake_get_user)) -> UserRole:
    return user.user_role


def fake_verify_customer(user=Depends(fake_get_user)) -> User:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    if not user.role == UserRole.CUSTOMER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden user")
    return user


def fake_verify_seller(user=Depends(fake_get_user)) -> User:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    if not user.role == UserRole.SELLER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden user")
    return user


def fake_verify_moderator(user=Depends(fake_get_user)) -> User:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    if not user.role == UserRole.MODERATOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden user")
    return user
