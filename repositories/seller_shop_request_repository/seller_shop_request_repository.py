from abc import ABC, abstractmethod

from domain.user import User
from repositories.seller_shop_request_repository.shop_creation_request import ShopCreationRequestInDB


class AsyncSellerShopRequestRepository(ABC):

    @abstractmethod
    async def create_shop_request(self, shop_request: ShopCreationRequestInDB) -> ShopCreationRequestInDB:
        pass

    @abstractmethod
    async def get_all_shop_requests(self, seller: User) -> list[ShopCreationRequestInDB]:
        pass

