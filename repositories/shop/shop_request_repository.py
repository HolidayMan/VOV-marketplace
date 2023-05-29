from abc import ABC, abstractmethod

from domain.request import ShopCreationRequest
from domain.user import User


class ShopRequestRepository(ABC):

    @abstractmethod
    def update(self, request: ShopCreationRequest) -> ShopCreationRequest:
        pass

    @abstractmethod
    def get_latest_request(self, seller: User) -> ShopCreationRequest:
        pass
