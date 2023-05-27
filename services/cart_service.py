from domain.user import User
from repositories.cart.cart_repository import CartRepository


class CartService:

    _repository: CartRepository = None

    def __init__(self, repository: CartRepository):
        self._repository = repository

    def get_cart_items(self, user: User):
        if user is None:
            # TODO: Replace with authorization exception
            raise Exception("User is None")
        items = self._repository.get_cart_items(user)
        return items

