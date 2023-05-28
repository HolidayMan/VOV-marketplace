from db import AsyncSession
from domain.product import Category, Product
from repositories.catalog.catalog_repository import CatalogRepository


class MySQLCatalogRepository(CatalogRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_catalog_items(self) -> list[Product]:
        async with self.session.cursor() as cursor:
            return []

    async def get_catalog_items_with_category(self, category_name: str) -> list[Product]:
        pass

    async def get_categories(self) -> list[Category]:
        pass