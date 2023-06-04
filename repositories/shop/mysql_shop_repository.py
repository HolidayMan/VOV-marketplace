from db import AsyncSession
from pydantic.types import PositiveInt
from domain.shop import Shop, ShopData
from domain.user import User
from repositories.shop.shop_repository import AsyncShopRepository

from repositories.shop.sql import INSERT_INTO_SHOP_DATA, INSERT_INTO_SHOP, SELECT_SHOP_BY_SELLER, UPDATE_SHOP_DATA_ID


# function converts a query result string into an object of type
def map_row_to_shop(row) -> Shop:
    shop_data = ShopData(
        name=row['name'],
        description=row['description'],
        approved=row['approved']
    )
    shop = Shop(
        shop_data=shop_data
    )
    return shop


class MySQLAsyncShopRepository(AsyncShopRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_shop(self, shop: Shop) -> Shop:
        async with self.session.cursor() as cursor:
            await cursor.execute(INSERT_INTO_SHOP, (shop.id, shop.shop_data.id))
            await self.session.commit()
        return shop

    async def get_shop_by_seller(self, seller: User) -> Shop | None:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                SELECT_SHOP_BY_SELLER,
                (seller.id,)
            )
            if show_row := await cursor.fetchone():
                shop = map_row_to_shop(show_row)
                return shop
        return None  # no shop for specific seller

    async def create_shop_data(self, shop_data: ShopData) -> ShopData:
        async with self.session.cursor() as cursor:
            shop_data_values = (shop_data.name, shop_data.description)
            await cursor.execute(INSERT_INTO_SHOP_DATA, shop_data_values)
            last_id = cursor.lastrowid
            shop_data.id = PositiveInt(last_id)
            await self.session.commit()
        return shop_data

    async def update_shop_date_id(self, shop_id: PositiveInt, shop_data_id: PositiveInt):
        async with self.session.cursor() as cursor:
            await cursor.execute(UPDATE_SHOP_DATA_ID, (shop_data_id, shop_id))
            await self.session.commit()
