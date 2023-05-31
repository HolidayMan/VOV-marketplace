from pydantic import PositiveInt
from pymysql.cursors import DictCursor

from db import AsyncSession
from domain.order import OrderItem
from domain.user import User
from repositories.order.seller_order.seller_order_repository import AsyncSellerOrderRepository


class MySQLAsyncSellerOrderRepository(AsyncSellerOrderRepository):

    def __init__(self, cursor: DictCursor):
        self.cursor = cursor

    async def get_ordered_items_list(self, seller: User) -> list[OrderItem]:
        pass

    async def get_ordered_item(self, order_id: PositiveInt) -> OrderItem:
        pass

    async def update_ordered_item(self, item: OrderItem) -> OrderItem:
        pass
