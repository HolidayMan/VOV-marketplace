from abc import ABC

from repositories.shop.mysql_shop_repository import MySQLAsyncShopRepository
from repositories.shop.shop_repository import AsyncShopRepository
from services.unit_of_work import MySQLAsyncUnitOfWork


class AbstractShopUnitOfWork(ABC):
    shop: AsyncShopRepository


class MySQLAsyncShopUnitOfWork(MySQLAsyncUnitOfWork, AbstractShopUnitOfWork):

    async def __aenter__(self):
        self.session = await self.session_factory()
        self.shop = MySQLAsyncShopRepository(self.session)
        await super().__aenter__()
