from abc import ABC, abstractmethod
from datetime import datetime

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
    async def decline_shop_request(self, shop_data_id: PositiveInt, refuse_reason: str,
                                   moderator: User, check_date: datetime) -> None:
        pass

    @abstractmethod
    async def approve_shop_request(self, shop_data_id: PositiveInt, moderator: User,
                                   check_date: datetime) -> None:
        pass
