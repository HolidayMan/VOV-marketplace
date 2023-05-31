from pymysql import DatabaseError

from domain.product import Product, Category
from services.exceptions import DataAccessError
from services.uow.catalog.catalog_unit_of_work import AbstractCatalogUnitOfWork


class CatalogService:

    _uow: AbstractCatalogUnitOfWork

    def __init__(self, unit_of_work: AbstractCatalogUnitOfWork):
        self._uow = unit_of_work

    async def get_catalog_items(self, category_name: str | None) -> list[Product]:
        try:
            async with self._uow:
                if category_name is not None:
                    return await self._uow.catalog.get_catalog_items_with_category(category_name)
                else:
                    return await self._uow.catalog.get_catalog_items()
        except DatabaseError:
            raise DataAccessError("Data access error")

    async def get_categories(self) -> list[Category]:
        try:
            async with self._uow:
                return await self._uow.catalog.get_categories()
        except DatabaseError:
            raise DataAccessError("Data access error")

