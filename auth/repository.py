from abc import ABC, abstractmethod

from pydantic import PositiveInt, EmailStr

from auth.exceptions import UserDoesNotExist, UserAlreadyExists
from auth.models import UserInDB
from db import AsyncSession
from domain.user import User, UserRole


class UserRepository(ABC):
    @abstractmethod
    def get_user_in_db(self, id_: PositiveInt) -> UserInDB:
        pass

    @abstractmethod
    def get_user(self, id_: PositiveInt) -> User:
        pass

    @abstractmethod
    def create_user(self, user: User, hashed_password: str) -> UserInDB:
        pass

    @abstractmethod
    def update_user(self, user: UserInDB) -> UserInDB:
        pass

    @abstractmethod
    def delete_user(self, user: UserInDB) -> None:
        pass

    @abstractmethod
    def find_user(self, email: str, role: UserRole) -> User | None:
        pass

    @abstractmethod
    def find_user_in_db(self, email: str, role: UserRole) -> UserInDB | None:
        pass

    def exists(self, id_: PositiveInt) -> bool:
        try:
            self.get_user_in_db(id_)
            return True
        except UserDoesNotExist:
            return False


class FakeUserRepository(UserRepository):
    def __init__(self, db: dict[PositiveInt, UserInDB] = None):
        if db is None:
            db = {}
        self.db = db

    def get_user(self, id_: PositiveInt) -> User:
        user = self.db.get(id_)
        if user is None:
            raise UserDoesNotExist("User does not exist")
        return user.to_user()

    def get_user_in_db(self, id_: PositiveInt) -> UserInDB:
        user = self.db.get(id_)
        if user is None:
            raise UserDoesNotExist("User does not exist")
        return user

    def create_user(self, user: User, hashed_password: str) -> UserInDB:
        if user.id:
            raise UserAlreadyExists("User already exists")
        if len(self.db.keys()) == 0:
            new_id = PositiveInt(1)
        else:
            new_id: PositiveInt = max(self.db.keys()) + 1
        user_in_db = UserInDB(**user.copy(update={'id': new_id}).dict(), hashed_password=hashed_password)
        self.db[new_id] = user_in_db
        return user_in_db

    def update_user(self, user: UserInDB) -> UserInDB:
        if user.id not in self.db:
            raise UserDoesNotExist("User does not exist")
        self.db[user.id] = user
        return user

    def delete_user(self, user: UserInDB) -> None:
        if user.id not in self.db:
            raise UserDoesNotExist("User does not exist")
        self.db.pop(user.id)

    def find_user(self, email: str, role: UserRole) -> User | None:
        if user := self.find_user_in_db(email, role):
            return user.to_user()
        return None

    def find_user_in_db(self, email: str, role: UserRole) -> UserInDB | None:
        for user in self.db.values():
            if user.email == email:
                return user
        return None


FAKE_REPO = FakeUserRepository(db={
        PositiveInt(1): UserInDB(
            id=PositiveInt(1),
            name="John Doe",
            email=EmailStr("example@gmail.com"),
            role=UserRole.CUSTOMER,
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
        )
    })


class MySQLUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_in_db(self, id_: PositiveInt) -> UserInDB:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                "SELECT id, name, email, role, password FROM users WHERE id = %s LIMIT 1",
                (id_,)
            )
            if user := await cursor.fetchone():
                return UserInDB(
                    id=PositiveInt(user['id']),
                    name=user['name'],
                    email=user['email'],
                    role=UserRole(user['role']),
                    hashed_password=user['password']
                )
            raise UserDoesNotExist("User does not exist")

    async def get_user(self, id_: PositiveInt) -> User:
        pass

    async def create_user(self, user: User, hashed_password: str) -> UserInDB:
        pass

    async def update_user(self, user: UserInDB) -> UserInDB:
        pass

    async def delete_user(self, user: UserInDB) -> None:
        pass

    async def find_user(self, email: str, role: UserRole) -> User | None:
        pass

    async def find_user_in_db(self, email: str, role: UserRole) -> UserInDB | None:
        pass
