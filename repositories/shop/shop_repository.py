from abc import ABC, abstractmethod

from pydantic import PositiveInt

from domain.shop import Shop
from domain.user import User
from repositories.seller_shop_request_repository.shop_creation_request import ShopCreationRequestInDB


class AsyncShopRepository(ABC):

    @abstractmethod
    async def create_shop(self, shop: Shop) -> Shop:
        pass

    @abstractmethod
    async def get_shop_by_seller(self, seller: User) -> Shop | None:
        pass

    @abstractmethod
    async def update_shop_date_id(self, shop_id: PositiveInt, shop_data_id: PositiveInt):
        pass

    @abstractmethod
    def create_shop_data(self, shop_data):
        pass

    @abstractmethod
    async def get_request_in_process(self, seller: User) -> ShopCreationRequestInDB | None:
        pass

