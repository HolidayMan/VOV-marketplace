from pydantic import BaseModel
from domain.types import PositiveInt, Email


class UserRole(BaseModel):
    id: PositiveInt | None = None
    name: str | None = None


class User(BaseModel):
    id: PositiveInt | None = None
    name: str | None = None
    email: Email | None = None
    user_role: UserRole | None = None


