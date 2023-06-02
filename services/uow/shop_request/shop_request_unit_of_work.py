from abc import ABC

from repositories.seller_shop_request_repository.mysql_seller_shop_request_repository import MySQLAsyncSellerShopRequestRepository
from repositories.seller_shop_request_repository.seller_shop_request_repository import AsyncSellerShopRequestRepository
from services.unit_of_work import MySQLAsyncUnitOfWork


class AbstractSellerShopRequestUnitOfWork(ABC):
    shop_request: AsyncSellerShopRequestRepository


class MySQLAsyncSellerShopRequestUnitOfWork(MySQLAsyncUnitOfWork, AbstractSellerShopRequestUnitOfWork):
    async def __aenter__(self):
        self.session = await self.session_factory()
        self.shop_request = MySQLAsyncSellerShopRequestRepository(self.session)
        await super().__aenter__()
