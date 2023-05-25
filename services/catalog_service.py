from domain.product import Product, Category
from repositories.catalog_repository import CatalogRepository
from repositories.fake_catalog_repository import FakeCatalogRepository


class CatalogService:

    __repository__: CatalogRepository = None

    def __init__(self, repository: CatalogRepository):
        self.__repository__ = repository

    def get_catalog_items(self) -> list[Product]:
        return self.__repository__.get_catalog_items()

    def get_catalog_items_by_category(self, category_name: str) -> list[Product]:
        return self.__repository__.get_catalog_items_with_category(category_name)

    def get_categories(self) -> list[Category]:
        return self.__repository__.get_categories()
