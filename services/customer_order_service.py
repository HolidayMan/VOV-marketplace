from pydantic import PositiveInt

from domain.order import Order
from domain.user import User
from services.uow.cart.cart_unit_of_work import AbstractCartUnitOfWork
from services.uow.customer_order.customer_order_unit_of_work import AbstractCustomerOrderUnitOfWork


class CustomerOrderService:

    _order_uow: AbstractCustomerOrderUnitOfWork
    _cart_uow: AbstractCartUnitOfWork

    def __init__(self, order_unit_of_work: AbstractCustomerOrderUnitOfWork,
                 cart_unit_of_work: AbstractCartUnitOfWork):
        self._order_uow = order_unit_of_work
        self._cart_uow = cart_unit_of_work

    async def make_order(self, user: User) -> Order:
        pass

    async def get_all_orders(self, user: User) -> list[Order]:
        pass

    async def get_order(self, user: User, orderId: PositiveInt) -> Order:
        pass
