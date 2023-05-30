from domain.shop import Shop, ShopData
from domain.user import User
from repositories.shop.mysql_shop_repository import MySQLAsyncShopRepository

from repositories.shop.shop_request_repository import ShopRequestRepository
from services.uow.shop.shop_unit_of_work import AbstractShopUnitOfWork


class ShopService:
    _ouw: AbstractShopUnitOfWork

    def __init__(self, unit_of_work: AbstractShopUnitOfWork):
        self._ouw = unit_of_work

    async def create_shop(self, name: str, description: str, seller: User) -> Shop:
        shop = Shop(id=seller.id,
                    shop_data=ShopData(name=name, description=description, approved=False))
        async with self._ouw:
            created_shop = await self._ouw.shop.create_shop(shop)
            return created_shop


    async def get_shop(self, seller: User):
        pass

    async def get_shop_creation_request(self, seller: User):
        pass
