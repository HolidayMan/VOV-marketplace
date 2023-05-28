from abc import ABC, abstractmethod

from pydantic import PositiveInt

from domain.cart import CartItem
from domain.user import User


class AsyncCartRepository(ABC):
    @abstractmethod
    async def get_cart_items(self, user: User) -> list[CartItem]:
        pass

    @abstractmethod
    async def add_cart_item(self, user: User, productId: PositiveInt, count: PositiveInt) -> CartItem:
        pass

    @abstractmethod
    async def remove_cart_item(self, user: User, productId: PositiveInt) -> bool:
        pass
