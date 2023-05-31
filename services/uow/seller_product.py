from abc import ABC

from repositories.seller_products.create_product_request import MySQLAsyncCreateProductRequestRepository
from services.unit_of_work import MySQLAsyncUnitOfWork, AsyncUnitOfWork


class AsyncProductCreationRequestUnitOfWork(AsyncUnitOfWork, ABC):
    products: MySQLAsyncCreateProductRequestRepository


class MySQLAsyncProductCreationRequestUnitOfWork(MySQLAsyncUnitOfWork, AsyncProductCreationRequestUnitOfWork):
    products: MySQLAsyncCreateProductRequestRepository

    async def __aenter__(self):
        if self.session is None or not self.session.is_active:
            self.session = await self.session_factory()
        self.cursor = await self.session.get_cursor()
        self.products = MySQLAsyncCreateProductRequestRepository(self.cursor)
        await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cursor.close()
        await super().__aexit__(exc_type, exc_val, exc_tb)
