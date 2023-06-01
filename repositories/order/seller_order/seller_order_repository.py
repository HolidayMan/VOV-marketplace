from abc import ABC, abstractmethod

from pydantic import PositiveInt

from domain.order import OrderStatus
from domain.user import User
from repositories.order.seller_order.order import OrderItemWithOrderIdAndCreationDate


class AsyncSellerOrderRepository(ABC):

    @abstractmethod
    async def get_ordered_items_list(self, seller: User) -> list[OrderItemWithOrderIdAndCreationDate]:
        pass

    @abstractmethod
    async def get_ordered_item(self, order_id: PositiveInt,
                               product_id: PositiveInt) -> OrderItemWithOrderIdAndCreationDate:
        pass

    @abstractmethod
    async def update_order_item(self,
                                order_item: OrderItemWithOrderIdAndCreationDate) -> OrderItemWithOrderIdAndCreationDate:
        pass

