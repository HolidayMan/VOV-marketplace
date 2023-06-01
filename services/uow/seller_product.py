from abc import ABC

from repositories.seller_products.create_product_request import MySQLAsyncProductManagementRepository, \
    AsyncProductManagementRepository
from services.unit_of_work import MySQLAsyncUnitOfWork, AsyncUnitOfWork


class AsyncProductManagementUnitOfWork(AsyncUnitOfWork, ABC):
    products: AsyncProductManagementRepository


class MySQLAsyncProductManagementUnitOfWork(MySQLAsyncUnitOfWork, AsyncProductManagementUnitOfWork):
    products: MySQLAsyncProductManagementRepository

    async def __aenter__(self):
        if self.session is None or not self.session.is_active:
            self.session = await self.session_factory()
        self.cursor = await self.session.get_cursor()
        self.products = MySQLAsyncProductManagementRepository(self.cursor)
        await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cursor.close()
        await super().__aexit__(exc_type, exc_val, exc_tb)
