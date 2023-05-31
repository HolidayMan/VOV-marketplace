from pydantic import PositiveInt

from domain.order import OrderItem
from domain.user import User


class SellerOrderService:

    async def get_ordered_items(self, seller: User) -> list[OrderItem]:
        pass

    async def get_ordered_item(self, seller: User, item_id: PositiveInt) -> OrderItem:
        pass

    async def accept_order(self, seller: User, item_id: PositiveInt) -> OrderItem:
        pass

    async def decline_order(self, seller: User, item_id: PositiveInt, refuse_reason: str) -> OrderItem:
        pass
