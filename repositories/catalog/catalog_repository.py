from abc import ABC, abstractmethod
from domain.product import Product, ProductData, Category


class AsyncCatalogRepository(ABC):
    @abstractmethod
    async def get_catalog_items(self) -> list[Product]:
        pass

    @abstractmethod
    async def get_catalog_items_with_category(self, category_name: str) -> list[Product]:
        pass

    @abstractmethod
    async def get_categories(self) -> list[Category]:
        pass
