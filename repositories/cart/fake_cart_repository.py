from money import Money
from pydantic import EmailStr, PositiveInt

from auth.exceptions import UserDoesNotExist
from domain.cart import CartItem
from domain.product import Product, ProductData
from domain.user import User, UserRole
from repositories.cart.cart_repository import AsyncCartRepository


class FakeAsyncCartRepository(AsyncCartRepository):

    def __init__(self, db: dict[User, list[CartItem]]):
        if db is None:
            db = {}
        self.db = db

    def get_cart_items(self, user: User) -> list[CartItem]:
        items = self.db.get(user)
        if items is None:
            raise UserDoesNotExist("User does not exist")
        return items

    def add_cart_item(self, user: User, item: CartItem) -> CartItem:
        if user not in self.db:
            raise UserDoesNotExist("User does not exist")
        return item

    def remove_cart_item(self, user: User, item: CartItem) -> bool:
        if item not in self.db.get(user):
            return False
        self.db.get(user).remove(item)
        return True


FAKE_CART_REPO = FakeAsyncCartRepository(db={
    User(
        id=PositiveInt(1),
        name="John Doe",
        email=EmailStr("example@gmail.com"),
        role=UserRole.CUSTOMER,
    ): [
        CartItem(
            product=Product(
                id=1,
                price=Money(2, "USD"),
                shop=1,
                product_data=ProductData(
                    id=1,
                    name="Apple",
                    description="something",
                    image_file_path="/apple.jpg",
                    approved=True
                )
            ),
            count=1,
            user_id=None
        ),
        CartItem(
            product=Product(
                id=2,
                price=Money(3, "USD"),
                shop=1,
                product_data=ProductData(
                    id=2,
                    name="Spiduh",
                    description="something",
                    image_file_path="/spiduh.jpg",
                    approved=True
                )
            ),
            count=1,
            user_id=None
        )
    ]
})
