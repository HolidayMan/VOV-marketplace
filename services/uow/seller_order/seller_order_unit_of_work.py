from abc import ABC

from repositories.order.seller_order.mysql_seller_order_repository import MySQLAsyncSellerOrderRepository
from repositories.order.seller_order.seller_order_repository import AsyncSellerOrderRepository
from services.unit_of_work import MySQLAsyncUnitOfWork


class AbstractSellerOrderUnitOfWork(ABC):
    orders: AsyncSellerOrderRepository


class MySQLAsyncCustomerOrderUnitOfWork(MySQLAsyncUnitOfWork, AbstractSellerOrderUnitOfWork):

    async def __aenter__(self):
        if self.session is None or not self.session.is_active:
            self.session = await self.session_factory()
        self.cursor = await self.session.get_cursor()
        self.products = MySQLAsyncSellerOrderRepository(self.cursor)
        await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cursor.close()
        await super().__aexit__(exc_type, exc_val, exc_tb)
