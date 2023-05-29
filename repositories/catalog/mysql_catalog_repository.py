from money import Money
from pydantic import PositiveInt

from db import AsyncSession
from domain.product import Category, Product, ProductData
from repositories.catalog.sql import SELECT_APPROVED_PRODUCTS_WITH_CATEGORY, SELECT_CATEGORIES, SELECT_APPROVED_PRODUCTS
from repositories.catalog.catalog_repository import AsyncCatalogRepository


def map_row_to_product(row) -> Product:
    return Product(
        id=PositiveInt(row['id']),
        price=Money(row['price'], 'UAH'),
        shop_id=PositiveInt(row['seller_id']),
        product_data=ProductData(
            id=PositiveInt(row['product_data_id']),
            name=row['name'],
            description=row['description'],
            image_file_path=row['image_file_path'],
            approved=True
        )
    )


def map_rows_to_products_list(product_rows) -> list[Product]:
    products_list = []
    for row in product_rows:
        product = map_row_to_product(row)
        products_list.append(product)
    return products_list


class MySQLAsyncCatalogRepository(AsyncCatalogRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_catalog_items(self) -> list[Product]:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                SELECT_APPROVED_PRODUCTS
            )
            if product_rows := await cursor.fetchall():
                products_list = map_rows_to_products_list(product_rows)
                return products_list
            return []

    async def get_catalog_items_with_category(self, category_name: str) -> list[Product]:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                SELECT_APPROVED_PRODUCTS_WITH_CATEGORY,
                (category_name,)
            )
            if product_rows := await cursor.fetchall():
                products_list = map_rows_to_products_list(product_rows)
                return products_list
            return []

    async def get_categories(self) -> list[Category]:
        async with self.session.cursor() as cursor:
            await cursor.execute(
                SELECT_CATEGORIES
            )
            if category_rows := await cursor.fetchall():
                categories_list = []
                for row in category_rows:
                    category = Category(
                        id=row['id'],
                        name=row['name']
                    )
                    categories_list.append(category)
                return categories_list
            return []
