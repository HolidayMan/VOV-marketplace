from pydantic import BaseModel
from pydantic import EmailStr
from pydantic.types import PositiveInt
from enum import Enum


class UserRole(Enum):
    CUSTOMER = "customer"
    SELLER = "seller"
    MODERATOR = "moderator"


class User(BaseModel):
    id: PositiveInt | None
    name: str
    email: EmailStr
    role: UserRole

    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id \
            and self.email == other.email and self.role == other.role

    def __hash__(self):
        return hash("".join([str(self.id), self.email, self.role.value]))
