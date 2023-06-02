from abc import ABC, abstractmethod

from pydantic import PositiveInt

from domain.shop import Shop, ShopData
from domain.user import User


class AsyncShopRepository(ABC):

    @abstractmethod
    async def create_shop(self, shop: Shop) -> Shop:
        pass

    @abstractmethod
    async def get_shop_by_seller(self, seller: User) -> Shop:
        pass

    @abstractmethod
    async def create_shop_data(self, shop_data: ShopData) -> ShopData:
        pass

    @abstractmethod
    async def update_shop_date_id(self, shop_id: PositiveInt, shop_data_id: PositiveInt):
        pass
