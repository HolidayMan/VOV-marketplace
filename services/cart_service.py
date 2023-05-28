from pydantic import PositiveInt

from domain.cart import CartItem
from domain.user import User
from auth.exceptions import UserIsNone
from services.uow.cart.cart_unit_of_work import AbstractCartUnitOfWork


class CartService:
    _uow: AbstractCartUnitOfWork

    def __init__(self, unit_of_work: AbstractCartUnitOfWork):
        self._uow = unit_of_work

    async def get_cart_items(self, user: User) -> list[CartItem]:
        async with self._uow:
            if user is None:
                raise UserIsNone("User is None")
            items = await self._uow.cart_items.get_cart_items(user)
            return items

    async def add_product(self, user: User, productId: PositiveInt, count: PositiveInt) -> CartItem:
        async with self._uow:
            if user is None:
                raise UserIsNone("User is None")
            added_item = await self._uow.cart_items.add_cart_item(user, productId, count)
            return added_item

    async def remove_item(self, user: User, productId: PositiveInt) -> bool:
        async with self._uow:
            if user is None:
                raise UserIsNone("User is None")
            removal_result = await self._uow.cart_items.remove_cart_item(user, productId)
            return removal_result
