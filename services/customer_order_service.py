from datetime import datetime

from pydantic import PositiveInt
from pymysql import ProgrammingError

from domain.cart import CartItem
from domain.order import Order, OrderStatus, OrderItem, OrderItemStatus
from domain.user import User
from services.exceptions import DataAccessError
from services.uow.cart.cart_unit_of_work import AbstractCartUnitOfWork
from services.uow.customer_order.customer_order_unit_of_work import AbstractCustomerOrderUnitOfWork


def make_order_items_from_cart_items(cart_items_list: list[CartItem]) -> list[OrderItem]:
    order_items_list = []
    for cart_item in cart_items_list:
        order_item = OrderItem(
            refuse_reason=None,
            product=cart_item.product,
            price=cart_item.price,
            check_date=None,
            status=OrderItemStatus.IN_PROCESS,
            count=cart_item.count
        )
        order_items_list.append(order_item)
    return order_items_list


class CustomerOrderService:

    _order_uow: AbstractCustomerOrderUnitOfWork
    _cart_uow: AbstractCartUnitOfWork

    def __init__(self, order_unit_of_work: AbstractCustomerOrderUnitOfWork,
                 cart_unit_of_work: AbstractCartUnitOfWork):
        self._order_uow = order_unit_of_work
        self._cart_uow = cart_unit_of_work

    async def make_order(self, user: User) -> Order:
        try:
            order: Order
            async with self._cart_uow:
                cart_items = await self._cart_uow.cart_items.get_cart_items(user)
                order_items = make_order_items_from_cart_items(cart_items)
                order = Order(user_id=user.id,
                              id=None,
                              order_items=order_items,
                              status=OrderStatus.IN_PROCESS,
                              creation_date=datetime.now(),)
            async with self._order_uow:
                order_in_db = await self._order_uow.orders.add_order(order)
                return order_in_db
        except ProgrammingError:
            raise DataAccessError("Data access error")

    async def get_all_orders(self, user: User) -> list[Order]:
        pass

    async def get_order(self, orderId: PositiveInt) -> Order:
        pass

    async def get_order_preview(self, user: User) -> Order:
        try:
            async with self._cart_uow:
                await self._cart_uow.cart_items.update_cart_items_prices(user)
                cart_items = await self._cart_uow.cart_items.get_cart_items(user)
                order_items = make_order_items_from_cart_items(cart_items)
                order = Order(user_id=user.id,
                              id=None,
                              order_items=order_items,
                              status=OrderStatus.IN_PROCESS,
                              creation_date=datetime.now(),)
                return order
        except ProgrammingError:
            raise DataAccessError("Data access error")

    async def can_make_order(self, user: User) -> bool:
        try:
            async with self._cart_uow:
                items = await self._cart_uow.cart_items.get_cart_items(user)
                if items:
                    return True
                else:
                    return False
        except ProgrammingError:
            raise DataAccessError("Data access error")
