from domain.product import Product, Category
from repositories.catalog_repository import CatalogRepository
from repositories.fake_catalog_repository import FakeCatalogRepository


class CatalogService:

    _repository: CatalogRepository = None

    def __init__(self, repository: CatalogRepository):
        self._repository = repository

    def get_catalog_items(self) -> list[Product]:
        return self._repository.get_catalog_items()

    def get_catalog_items_by_category(self, category_name: str) -> list[Product]:
        return self._repository.get_catalog_items_with_category(category_name)

    def get_categories(self) -> list[Category]:
        return self._repository.get_categories()
