from pydantic import PositiveInt
from pymysql import ProgrammingError

from domain.cart import CartItem
from domain.user import User
from services.exceptions import DataAccessError
from services.uow.cart.cart_unit_of_work import AbstractCartUnitOfWork


class CartService:
    _uow: AbstractCartUnitOfWork

    def __init__(self, unit_of_work: AbstractCartUnitOfWork):
        self._uow = unit_of_work

    async def get_cart_items(self, user: User) -> list[CartItem]:
        async with self._uow:
            return await self.wrapper(
                self._uow.cart_items.get_cart_items,
                user
            )

    async def add_product(self, user: User, productId: PositiveInt, count: PositiveInt) -> CartItem:
        async with self._uow:
            return await self.wrapper(
                self._uow.cart_items.add_cart_item,
                user,
                productId,
                count
            )

    async def remove_item(self, user: User, productId: PositiveInt) -> bool:
        async with self._uow:
            return await self.wrapper(
                self._uow.cart_items.remove_cart_item,
                user,
                productId
            )

    async def wrapper(self, method, *args, **kwargs):
        try:
            return await method(*args, **kwargs)
        except ProgrammingError:
            raise DataAccessError("Data access error")

