from pydantic import PositiveInt

from db import AsyncSession
from domain.order import Order
from domain.user import User
from repositories.customer_order.customer_order_repository import AsyncCustomerOrderRepository


class MySQLAsyncCustomerOrderRepository(AsyncCustomerOrderRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_orders(self, user: User) -> list[Order]:
        pass

    async def get_order(self, orderId: PositiveInt) -> Order:
        pass

    async def add_order(self, order: Order) -> Order:
        pass
