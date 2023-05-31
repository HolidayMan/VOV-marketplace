from abc import ABC, abstractmethod

from pydantic import PositiveInt

from domain.order import OrderItem
from domain.user import User


class AsyncSellerOrderRepository(ABC):

    @abstractmethod
    async def get_ordered_items_list(self, seller: User) -> list[OrderItem]:
        pass

    @abstractmethod
    async def get_ordered_item(self, order_id: PositiveInt) -> OrderItem:
        pass

    @abstractmethod
    async def update_ordered_item(self, item: OrderItem) -> OrderItem:
        pass
