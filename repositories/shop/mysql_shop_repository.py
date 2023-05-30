from db import AsyncSession
from pydantic.types import PositiveInt
from domain.shop import Shop
from domain.user import User
from repositories.shop.shop_repository import AsyncShopRepository

from repositories.shop.sql import INSERT_INTO_SHOP_DATA, INSERT_INTO_SHOP


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

    async def get_shop(self, seller: User) -> Shop:
        pass
