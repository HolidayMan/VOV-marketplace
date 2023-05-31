from pymysql import ProgrammingError, IntegrityError

from domain.shop import Shop, ShopData
from domain.user import User
from repositories.shop.mysql_shop_repository import MySQLAsyncShopRepository

from repositories.shop.shop_request_repository import ShopRequestRepository
from services.exceptions import DataAccessError, CannotCreateShopError
from services.uow.shop.shop_unit_of_work import AbstractShopUnitOfWork


class ShopService:
    _ouw: AbstractShopUnitOfWork

    def __init__(self, unit_of_work: AbstractShopUnitOfWork):
        self._ouw = unit_of_work

    async def create_shop(self, name: str, description: str, seller: User) -> Shop:
        try:
            has_shop = await self.check_seller_has_shop(seller)
            if has_shop:
                raise DataAccessError("Seller already has a shop")
            else:
                shop = Shop(id=seller.id,
                            shop_data=ShopData(name=name, description=description, approved=False))

                async with self._ouw:
                    created_shop = await self._ouw.shop.create_shop(shop)
                    return created_shop
        except ProgrammingError:
            raise DataAccessError("Data access error")
        except IntegrityError:
            raise CannotCreateShopError("Seller already has a shop")

    async def get_shop_by_seller(self, seller: User):
        try:
            async with self._ouw:
                shop = await self._ouw.shop.get_shop_by_seller(seller)
                return shop
        except ProgrammingError:
            raise DataAccessError("Data access error")

    async def check_seller_has_shop(self, seller: User) -> bool:
        try:
            async with self._ouw:
                existing_shop = await self._ouw.shop.get_shop_by_seller(seller)
                return existing_shop is not None
        except ProgrammingError:
            raise DataAccessError("Data access error")
