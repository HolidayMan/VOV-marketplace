from abc import ABC, abstractmethod

from pydantic import PositiveInt, EmailStr

from auth.exceptions import UserDoesNotExist, UserAlreadyExists
from auth.models import UserInDB
from auth.sql import SELECT_USER_BY_ID, SELECT_USER_BY_EMAIL_AND_ROLE, INSERT_NEW_USER,\
    UPDATE_USER, DELETE_USER
from db import AsyncSession
from domain.user import User, UserRole


class AsyncUserRepository(ABC):
    @abstractmethod
    async def get_user_in_db(self, id_: PositiveInt) -> UserInDB:
        pass

    @abstractmethod
    async def get_user(self, id_: PositiveInt) -> User:
        pass

    @abstractmethod
    async def create_user(self, user: User, hashed_password: str) -> UserInDB:
        pass

    @abstractmethod
    async def update_user(self, user: UserInDB) -> UserInDB:
        pass

    @abstractmethod
    async def delete_user(self, user: UserInDB) -> None:
        pass

    @abstractmethod
    async def find_user(self, email: str, role: UserRole) -> User | None:
        pass

    @abstractmethod
    async def find_user_in_db(self, email: str, role: UserRole) -> UserInDB | None:
        pass

    async def exists(self, id_: PositiveInt) -> bool:
        try:
            await self.get_user_in_db(id_)
            return True
        except UserDoesNotExist:
            return False


class FakeUserRepository(AsyncUserRepository):
    def __init__(self, db: dict[PositiveInt, UserInDB] = None):
        if db is None:
            db = {}
        self.db = db

    async def get_user(self, id_: PositiveInt) -> User:
        user = self.get_user_in_db(id_)
        return user.to_user()

    async def get_user_in_db(self, id_: PositiveInt) -> UserInDB:
        user = self.db.get(id_)
        if user is None:
            raise UserDoesNotExist("User does not exist")
        return user

    async def create_user(self, user: User, hashed_password: str) -> UserInDB:
        if user.id:
            raise UserAlreadyExists("User already exists")
        if len(self.db.keys()) == 0:
            new_id = PositiveInt(1)
        else:
            new_id: PositiveInt = max(self.db.keys()) + 1
        user_in_db = UserInDB(**user.copy(update={'id': new_id}).dict(), hashed_password=hashed_password)
        self.db[new_id] = user_in_db
        return user_in_db

    async def update_user(self, user: UserInDB) -> UserInDB:
        if user.id not in self.db:
            raise UserDoesNotExist("User does not exist")
        self.db[user.id] = user
        return user

    async def delete_user(self, user: UserInDB) -> None:
        if user.id not in self.db:
            raise UserDoesNotExist("User does not exist")
        self.db.pop(user.id)

    async def find_user(self, email: str, role: UserRole) -> User | None:
        if user := self.find_user_in_db(email, role):
            return user.to_user()
        return None

    async def find_user_in_db(self, email: str, role: UserRole) -> UserInDB | None:
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


class MySQLUserRepository(AsyncUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_in_db(self, id_: PositiveInt) -> UserInDB:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                SELECT_USER_BY_ID,
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
        user = await self.get_user_in_db(id_)
        return user.to_user()

    async def create_user(self, user: User, hashed_password: str) -> UserInDB:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                INSERT_NEW_USER,
                (user.name, user.email, hashed_password, user.role.value)
            )
            await self.session.commit()
            return UserInDB(
                id=PositiveInt(cursor.lastrowid),
                name=user.name,
                email=user.email,
                role=user.role,
                hashed_password=hashed_password
            )

    async def update_user(self, user: UserInDB) -> UserInDB:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                UPDATE_USER,
                (user.name, user.email, user.hashed_password, user.role.value, user.id)
            )
            await self.session.commit()
            return user

    async def delete_user(self, user: UserInDB) -> None:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                DELETE_USER,
                (user.id,)
            )
            await self.session.commit()

    async def find_user(self, email: str, role: UserRole) -> User | None:
        user = await self.find_user_in_db(email, role)
        if user:
            return user.to_user()
        return None

    async def find_user_in_db(self, email: str, role: UserRole) -> UserInDB | None:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                SELECT_USER_BY_EMAIL_AND_ROLE,
                (email, role.value)
            )
            if user := await cursor.fetchone():
                return UserInDB(
                    id=PositiveInt(user['id']),
                    name=user['name'],
                    email=user['email'],
                    role=UserRole(user['role']),
                    hashed_password=user['password']
                )
            return None
