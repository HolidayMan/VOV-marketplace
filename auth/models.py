from pydantic import BaseModel, PositiveInt, EmailStr

from domain.user import User, UserRole


class UserTokenData(BaseModel):
    sub: EmailStr
    role: UserRole

    class Config:
        use_enum_values = True


class UserInDB(User):
    id: PositiveInt
    hashed_password: str

    def to_user(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            email=self.email,
            role=self.role
        )
