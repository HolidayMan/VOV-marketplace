from abc import ABC

from repositories.cart.cart_repository import AsyncCartRepository
from repositories.cart.mysql_cart_repository import MySQLAsyncCartRepository
from services.unit_of_work import MySQLAsyncUnitOfWork


class AbstractCartUnitOfWork(ABC):
    cart_items: AsyncCartRepository


class MySQLAsyncCartUnitOfWork(MySQLAsyncUnitOfWork, AbstractCartUnitOfWork):

    async def __aenter__(self):
        self.session = await self.session_factory()
        self.cart_items = MySQLAsyncCartRepository(self.session)
        await super().__aenter__()
