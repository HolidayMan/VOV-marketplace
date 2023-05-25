from domain.product import Product, Category
from repositories.catalog_repository import CatalogRepository
from repositories.fake_catalog_repository import FakeCatalogRepository


class CatalogService:

    _repository: CatalogRepository = None

    def __init__(self, repository: CatalogRepository):
        self._repository = repository

    def get_catalog_items(self, category_name: str | None) -> list[Product]:
        if category_name is not None:
            return self._repository.get_catalog_items_with_category(category_name)
        else:
            return self._repository.get_catalog_items()

    def get_categories(self) -> list[Category]:
        return self._repository.get_categories()
