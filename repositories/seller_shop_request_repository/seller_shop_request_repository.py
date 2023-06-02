from abc import ABC, abstractmethod

from pydantic import PositiveInt

from domain.request import ShopCreationRequest
from domain.shop import ShopData, Shop
from domain.user import User
from repositories.seller_shop_request_repository.shop_creation_request import ShopCreationRequestInDB


class AsyncSellerShopRequestRepository(ABC):

    @abstractmethod
    async def update(self, request: ShopCreationRequestInDB) -> ShopCreationRequestInDB:
        pass

    @abstractmethod
    async def get_latest_request(self, seller: User) -> ShopCreationRequestInDB:
        pass

    @abstractmethod
    async def create_shop_request(self, shop_request: ShopCreationRequestInDB) -> ShopCreationRequestInDB:
        pass

    @abstractmethod
    async def get_shop_request_by_shop_data(self, shop_data: ShopData) -> ShopCreationRequestInDB:
        pass

    @abstractmethod
    async def get_all_shop_requests(self, seller: User) -> list[ShopCreationRequestInDB]:
        pass


