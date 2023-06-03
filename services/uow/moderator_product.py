from abc import ABC, abstractmethod

from repositories.moderator_products.product_request_approval_repository import AsyncProductRequestApprovalRepository, \
    MySQLAsyncProductRequestApprovalRepository
from services.unit_of_work import MySQLAsyncUnitOfWork, AsyncUnitOfWork


class AsyncModeratorProductUnitOfWork(AsyncUnitOfWork, ABC):

    @property
    @abstractmethod
    def requests(self) -> AsyncProductRequestApprovalRepository:
        pass


class MySQLAsyncModeratorProductUnitOfWork(MySQLAsyncUnitOfWork, AsyncModeratorProductUnitOfWork):

    @property
    def requests(self) -> MySQLAsyncProductRequestApprovalRepository:
        return self._requests

    async def __aenter__(self):
        if self.session is None or not self.session.is_active:
            self.session = await self.session_factory()
        self.cursor = await self.session.get_cursor()
        self._requests = MySQLAsyncProductRequestApprovalRepository(self.cursor)
        await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cursor.close()
        await super().__aexit__(exc_type, exc_val, exc_tb)
