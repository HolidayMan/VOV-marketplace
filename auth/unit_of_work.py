from auth.repository import UserRepository
from db import AsyncSession, DEFAULT_SESSION_FACTORY
from .repository import MySQLUserRepository
from services.unit_of_work import MySQLAsyncUnitOfWork


class MySQLAsyncUserUnitOfWork(MySQLAsyncUnitOfWork):
    users: MySQLUserRepository

    async def __aenter__(self):
        self.session = await self.session_factory()
        self.users = MySQLUserRepository(self.session)
        await super().__aenter__()
