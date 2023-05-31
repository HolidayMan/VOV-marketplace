from db import AsyncSession
from pydantic.types import PositiveInt
from domain.shop import Shop, ShopData
from domain.user import User
from repositories.shop.shop_repository import AsyncShopRepository

from repositories.shop.sql import INSERT_INTO_SHOP_DATA, INSERT_INTO_SHOP, SELECT_SHOP_BY_SELLER


# function converts a query result string into an object of type
def map_row_to_shop(row) -> Shop:
    shop_data = ShopData(
        name=row['name'],
        description=row['description'],
        approved=False
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
            shop_data_values = (shop.shop_data.name, shop.shop_data.description)
            await cursor.execute(INSERT_INTO_SHOP_DATA, shop_data_values)
            # Получение последнего автоматически сгенерированного значения для id вставленной строки
            last_id = cursor.lastrowid
            shop_values_with_fk = (shop.id, last_id)
            await cursor.execute(INSERT_INTO_SHOP, shop_values_with_fk)
            await self.session.commit()
            shop.shop_data.id = PositiveInt(last_id)
        return shop

    async def get_shop_by_seller(self, seller: User) -> Shop | None:
        print("hiiii")
        async with self.session.cursor() as cursor:
            await cursor.execute(
                SELECT_SHOP_BY_SELLER,
                (seller.id,)
            )
            print("i am here")
            if show_row := await cursor.fetchone():
                print("i still here")
                shop = map_row_to_shop(show_row)
                print("everything fine!")
                return shop
        return None  # no shop for specific seller
