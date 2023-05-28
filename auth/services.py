from datetime import timedelta

from pydantic import EmailStr

from .exceptions import CredentialsInvalid
from .logic import authenticate_user, create_access_token, create_user
from .unit_of_work import AsyncUserUnitOfWork
from .models import UserTokenData, UserInDB
from domain.user import UserRole, User
from settings import ACCESS_TOKEN_EXPIRE_MINUTES


async def process_user_login(uow: AsyncUserUnitOfWork, email: EmailStr, password: str, role: UserRole) -> dict[str, str]:
    user = await authenticate_user(uow, email, role, password)
    if not user:
        raise CredentialsInvalid("invalid credentials")
    access_token = create_access_token(data=UserTokenData(sub=email, role=role),
                                       expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}


async def process_create_user(uow: AsyncUserUnitOfWork, user: User, password: str) -> dict[str, str]:
    user = await create_user(uow, user, password)
    access_token = create_access_token(data=UserTokenData(sub=user.email, role=user.role),
                                       expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}
