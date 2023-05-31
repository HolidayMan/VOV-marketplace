from abc import ABC

from repositories.customer_order.customer_order_repository import AsyncCustomerOrderRepository
from repositories.customer_order.mysql_customer_order_repository import MySQLAsyncCustomerOrderRepository
from services.unit_of_work import MySQLAsyncUnitOfWork


class AbstractCustomerOrderUnitOfWork(ABC):
    orders: AsyncCustomerOrderRepository


class MySQLAsyncCustomerOrderUnitOfWork(MySQLAsyncUnitOfWork, AbstractCustomerOrderUnitOfWork):

    async def __aenter__(self):
        self.session = await self.session_factory()
        self.orders = MySQLAsyncCustomerOrderRepository(self.session)
        await super().__aenter__()
