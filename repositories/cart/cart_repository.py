from abc import ABC, abstractmethod
from domain.cart import CartItem
from domain.user import User


class CartRepository(ABC):
    @abstractmethod
    def get_cart_items(self, user: User) -> list[CartItem]:
        pass

    @abstractmethod
    def add_cart_item(self, user: User, item: CartItem) -> CartItem:
        pass

    @abstractmethod
    def remove_cart_item(self, user: User, item: CartItem) -> bool:
        pass
