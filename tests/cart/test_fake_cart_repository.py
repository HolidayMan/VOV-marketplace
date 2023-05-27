import pytest
from money import Money

from domain.product import Product, ProductData
from repositories.cart.fake_cart_repository import FakeCartRepository
from domain.cart import CartItem
from domain.user import User, UserRole


@pytest.fixture
def mock_user():
    return User(
        id=1,
        name="Someone",
        email="some@gmail.com",
        role=UserRole.CUSTOMER
    )

@pytest.fixture
def mock_cart_items():
    return [
        CartItem(
            product=Product(
                id=1,
                price=Money(2, "USD"),
                shop_id=1,
                product_data=ProductData(
                    id=1,
                    name="Apple",
                    description="something",
                    image_file_path="/someimg.jpg",
                    approved=True
                )
            )
        )
    ]

