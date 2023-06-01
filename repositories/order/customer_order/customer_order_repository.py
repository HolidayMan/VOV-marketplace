from abc import ABC, abstractmethod

from pydantic import PositiveInt

from domain.order import Order
from domain.user import User


class AsyncCustomerOrderRepository(ABC):

    @abstractmethod
    async def get_all_orders(self, user: User) -> list[Order]:
        pass

    @abstractmethod
    async def get_order(self, orderId: PositiveInt) -> Order:
        pass

    @abstractmethod
    async def add_order(self, order: Order, user: User) -> Order:
        pass
    