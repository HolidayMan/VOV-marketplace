from abc import ABC

from repositories.moderator_shop_request_repository.moderator_shop_request_repository import \
    AsyncModeratorShopRequestRepository
from repositories.moderator_shop_request_repository.mysql_moderator_shop_request_repository import \
    MYSQLAsyncModeratorShopRequestRepository
from services.unit_of_work import MySQLAsyncUnitOfWork, AsyncUnitOfWork


class AbstractModeratorShopRequestUnitOfWork(AsyncUnitOfWork, ABC):
    shop_request: AsyncModeratorShopRequestRepository


class MySQLAsyncModeratorShopRequestUnitOfWork(MySQLAsyncUnitOfWork, AbstractModeratorShopRequestUnitOfWork):
    async def __aenter__(self):
        if self.session is None or not self.session.is_active:
            self.session = await self.session_factory()
        self.cursor = await self.session.get_cursor()
        self.shop_request = MYSQLAsyncModeratorShopRequestRepository(self.cursor)
        await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cursor.close()
        await super().__aexit__(exc_type, exc_val, exc_tb)
