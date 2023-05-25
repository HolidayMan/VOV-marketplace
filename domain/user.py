from pydantic import BaseModel
from domain.types import PositiveInt, Email
from enum import Enum


class UserRole(Enum):
    CUSTOMER = "customer"
    SELLER = "seller"
    MODERATOR = "moderator"


class User(BaseModel):
    id: PositiveInt
    name: str
    email: Email
    user_role: UserRole


