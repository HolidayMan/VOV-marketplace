from abc import ABC, abstractmethod
from pydantic import PositiveInt
from domain.user import User
from repositories.seller_shop_request_repository.shop_creation_request import ShopCreationRequestInDB


class AsyncModeratorShopRequestRepository(ABC):
    @abstractmethod
    async def get_shop_requests_list(self) -> list[ShopCreationRequestInDB]:
        pass

    @abstractmethod
    async def get_shop_request(self, shop_data_id: PositiveInt) -> ShopCreationRequestInDB:
        pass

    @abstractmethod
    async def update_shop_request_status(self, shop_request: ShopCreationRequestInDB) -> ShopCreationRequestInDB:
        pass
