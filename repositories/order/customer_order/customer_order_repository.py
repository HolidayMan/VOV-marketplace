from abc import ABC, abstractmethod

from pydantic import PositiveInt

from domain.order import Order
from domain.user import User
from repositories.order.order import OrderWithUserId


class AsyncCustomerOrderRepository(ABC):

    @abstractmethod
    async def get_all_orders(self, user: User) -> list[OrderWithUserId]:
        pass

    @abstractmethod
    async def get_order(self, orderId: PositiveInt) -> OrderWithUserId:
        pass

    @abstractmethod
    async def add_order(self, order: Order, user: User) -> OrderWithUserId:
        pass

    @abstractmethod
    async def cancel_order(self, orderId: PositiveInt) -> OrderWithUserId:
        pass
    