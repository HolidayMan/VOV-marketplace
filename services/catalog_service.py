from domain.product import Product, Category
from services.uow.catalog.catalog_unit_of_work import AbstractCatalogUnitOfWork


class CatalogService:

    _uow: AbstractCatalogUnitOfWork

    def __init__(self, unit_of_work: AbstractCatalogUnitOfWork):
        self._uow = unit_of_work

    async def get_catalog_items(self, category_name: str | None) -> list[Product]:
        async with self._uow:
            if category_name is not None:
                return self._uow.catalog.get_catalog_items_with_category(category_name)
            else:
                return self._uow.catalog.get_catalog_items()

    async def get_categories(self) -> list[Category]:
        async with self._uow:
            return self._uow.catalog.get_categories()
