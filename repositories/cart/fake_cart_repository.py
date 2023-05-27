from domain.cart import CartItem
from domain.user import User
from repositories.cart.cart_repository import CartRepository


class FakeCartRepository(CartRepository):

    cart_items: list[CartItem]

    def get_cart_items(self, user: User) -> list[CartItem]:
        return self.cart_items

    def add_cart_item(self, user: User, item: CartItem) -> CartItem:
        self.cart_items.append(item)
        item.user_id = user.id
        return item

    def remove_cart_item(self, user: User, item: CartItem) -> bool:
        self.cart_items.remove(item)
        return True
