from abc import ABC, abstractmethod
from domain.shop import Shop, ShopData
from domain.user import User


class ShopRepository(ABC):

    @abstractmethod
    def create(self, shop: Shop) -> Shop:
        pass

    @abstractmethod
    def get(self, seller: User) -> Shop:
        pass
