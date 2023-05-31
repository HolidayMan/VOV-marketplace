from abc import ABC, abstractmethod
from domain.shop import Shop, ShopData
from domain.user import User


class AsyncShopRepository(ABC):

    @abstractmethod
    async def create_shop(self, shop: Shop) -> Shop:
        pass

    @abstractmethod
    async def get_shop_by_seller(self, seller: User) -> Shop:
        pass
