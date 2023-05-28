from pydantic import PositiveInt

from domain.cart import CartItem
from domain.user import User
from auth.exceptions import UserIsNone
from repositories.cart.cart_repository import CartRepository


class CartService:
    _repository: CartRepository = None

    def __init__(self, repository: CartRepository):
        self._repository = repository

    def get_cart_items(self, user: User) -> list[CartItem]:
        if user is None:
            raise UserIsNone("User is None")
        items = self._repository.get_cart_items(user)
        return items

    def add_product(self, user: User, productId: PositiveInt, count: PositiveInt) -> CartItem:
        pass

    def remove_item(self, itemId: PositiveInt) -> bool:
        pass
