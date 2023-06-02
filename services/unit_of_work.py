from abc import ABC, abstractmethod

from db import DEFAULT_SESSION_FACTORY, AsyncSession


class AsyncUnitOfWork(ABC):

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass


class MySQLAsyncUnitOfWork(AsyncUnitOfWork, ABC):
    """
    Example of inheritance:
    class MySQLAsyncProductManagementUnitOfWork(MySQLAsyncUnitOfWork):
        users: MySQLUserRepository

        async def __aenter__(self):
            self.session = await self.session_factory()
            self.users = MySQLUserRepository(self.session)
            await super().__aenter__()
    """
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
