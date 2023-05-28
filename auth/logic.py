from datetime import timedelta, datetime

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr

from auth.exceptions import UserAlreadyExists
from auth.models import UserInDB, UserTokenData
from .unit_of_work import AsyncUserUnitOfWork
from domain.user import UserRole, User
from settings import SECRET_KEY, HASHING_ALGORITHM, CRYPT_CONTEXT_SCHEMES

pwd_context = CryptContext(schemes=CRYPT_CONTEXT_SCHEMES, deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(uow: AsyncUserUnitOfWork, email: EmailStr, role: UserRole) -> UserInDB | None:
    """gets user from repository by email and role"""
    async with uow:
        return await uow.users.find_user_in_db(email, role)


async def authenticate_user(uow: AsyncUserUnitOfWork, email: EmailStr, role: UserRole, password: str) -> UserInDB | None:
    """
    authenticates user by email and role
    returns user if password is correct otherwise returns None
    """
    user = await get_user(uow, email, role)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: UserTokenData, expires_delta: timedelta | None = None):
    """
    creates access token for given data and expiration time
    """
    to_encode = data.dict()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASHING_ALGORITHM)
    return encoded_jwt


async def get_user_by_token(uow: AsyncUserUnitOfWork, token: str) -> UserInDB | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            return None
    except JWTError:
        return None
    try:
        user_role = UserRole(role)
    except ValueError:
        return None
    user = await get_user(uow, EmailStr(email), user_role)
    return user


async def create_user(uow: AsyncUserUnitOfWork, user: User, password: str) -> UserInDB:
    """
    creates user in repository
    """
    async with uow:
        if await uow.users.find_user_in_db(user.email, user.role):
            raise UserAlreadyExists("user already exists")
        hashed_password = get_password_hash(password)
        return await uow.users.create_user(user, hashed_password)
