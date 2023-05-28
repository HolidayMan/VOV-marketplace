from pydantic import PositiveInt
from db import AsyncSession
from domain.cart import CartItem
from domain.product import Product, ProductData
from domain.user import User
from repositories.cart.sql import SELECT_CART_ITEMS, INSERT_CART_ITEM, DELETE_CART_ITEM, GET_CART_ITEM
from repositories.cart.cart_repository import AsyncCartRepository


def map_row_to_cart_item(row) -> CartItem:
    return CartItem(
        product=Product(
            id=row['product_id'],
            price=row['price'],
            shop_id=row['seller_id'],
            product_data=ProductData(
                id=row['product_data_id'],
                name=row['name'],
                description=row['description'],
                image_file_path=row['image_file_path'],
                approved=row['approved']
            )
        ),
        count=row['count'],
        user_id=row['customer_id']
    )


def map_rows_to_cart_items_list(cart_items_rows) -> list[CartItem]:
    cart_items_list = []
    for row in cart_items_rows:
        item = map_row_to_cart_item(row)
        cart_items_list.append(item)
    return cart_items_list


class MySQLAsyncCartRepository(AsyncCartRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_single_cart_item(self, user: User, productId: PositiveInt) -> CartItem | None:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                GET_CART_ITEM,
                (user.id, productId)
            )
            if item := await cursor.fetchone():
                return item
            return None

    async def get_cart_items(self, user: User) -> list[CartItem]:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                SELECT_CART_ITEMS,
                (user.id,)
            )
            if cart_item_rows := await cursor.fetchall():
                cart_items_list = map_rows_to_cart_items_list(cart_item_rows)
                return cart_items_list
            return []

    async def add_cart_item(self, user: User, productId: PositiveInt, count: PositiveInt) -> CartItem:
        async with self.session.cursor() as cursor:
            if item := await self.get_single_cart_item(user, productId):
                count += item.count
                await self.remove_cart_item(user, productId)
            await cursor.execute(
                INSERT_CART_ITEM,
                (count, productId, user.id)
            )
            await self.session.commit()
            item_to_return = await self.get_single_cart_item(user, productId)
            return item_to_return

    async def remove_cart_item(self, user: User, productId: PositiveInt) -> bool:
        async with self.session.cursor() as cursor:
            item = await self.get_single_cart_item(user, productId)
            if item is None:
                return False
            await cursor.execute(
                DELETE_CART_ITEM,
                (user.id, productId)
            )
            await self.session.commit()
            return True



