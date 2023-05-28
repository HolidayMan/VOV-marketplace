from abc import ABC, abstractmethod
from .repository import MySQLUserRepository
from services.unit_of_work import MySQLAsyncUnitOfWork, AsyncUnitOfWork


class AsyncUserUnitOfWork(AsyncUnitOfWork, ABC):
    users: MySQLUserRepository


class MySQLAsyncUserUnitOfWork(MySQLAsyncUnitOfWork, AsyncUserUnitOfWork):
    users: MySQLUserRepository

    async def __aenter__(self):
        self.session = await self.session_factory()
        self.users = MySQLUserRepository(self.session)
        await super().__aenter__()
