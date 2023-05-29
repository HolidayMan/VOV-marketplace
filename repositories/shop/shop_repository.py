from abc import ABC, abstractmethod
from domain.shop import Shop, ShopData
from domain.user import User


class ShopRepository(ABC):

    @abstractmethod
    def create_shop(self, shop: Shop) -> Shop:
        pass

    @abstractmethod
    def get_shop(self, seller: User) -> Shop:
        pass
