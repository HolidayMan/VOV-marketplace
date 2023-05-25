from domain.product import Product, Category
from repositories.catalog_repository import CatalogRepository
from repositories.fake_catalog_repository import FakeCatalogRepository


class CatalogService:
    __repository__: CatalogRepository = None

    def __init__(self, repository: CatalogRepository):
        self.__repository__ = repository

    def get_catalog_items(self, category_name: str | None) -> list[Product]:
        if category_name is not None:
            return self.__repository__.get_catalog_items_with_category(category_name)
        else:
            return self.__repository__.get_catalog_items()

    def get_categories(self) -> list[Category]:
        return self.__repository__.get_categories()
