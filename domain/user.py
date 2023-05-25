from pydantic import BaseModel
from domain.types import ID


class UserRole(BaseModel):
    id: ID | None = None
    name: str | None = None


class User(BaseModel):
    id: ID | None = None
    name: str | None = None
    email: str | None = None
    user_role: UserRole | None = None


