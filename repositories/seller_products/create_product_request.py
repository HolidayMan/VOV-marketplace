from abc import ABC, abstractmethod

from aiomysql import DictCursor
from pydantic.types import PositiveInt

from db import AsyncSession
from domain.product import Product, Category, ProductWithCategories
from domain.request import ProductCreationRequest, RequestStatus
from domain.shop import Shop
from .sql import INSERT_PRODUCT_DATA, INSERT_ADD_PRODUCT_REQUEST, INSERT_PRODUCT, INSERT_PRODUCT_CATEGORIES


class ProductWithShopId(Product):
    shop_id: PositiveInt
    shop: None = None


class ProductWithShopIdAndCategoriesIds(ProductWithShopId):
    categories_ids: list[PositiveInt]


class AsyncCreateProductRequestRepository(ABC):

    @abstractmethod
    async def create_product_request(self, product_request: ProductCreationRequest) -> ProductCreationRequest:
        pass

    @abstractmethod
    async def create_product(self, product: ProductWithShopId) -> bool:
        pass

    @abstractmethod
    async def get_current_product_request(self, product_request_id: int) -> ProductCreationRequest:
        pass

    @abstractmethod
    async def get_all_product_requests(self, product: Product) -> list[ProductCreationRequest]:
        pass

    @abstractmethod
    async def update_product_request(self, product_request: ProductCreationRequest) -> ProductCreationRequest:
        pass

    @abstractmethod
    async def get_product_request_satus(self, product_request: ProductCreationRequest) -> RequestStatus:
        pass


class MySQLAsyncCreateProductRequestRepository(AsyncCreateProductRequestRepository):
    def __init__(self, cursor: DictCursor):
        self.cursor = cursor

    async def create_product_request(self, product_request: ProductCreationRequest) -> ProductCreationRequest:
        product_request = product_request.copy()
        await self.cursor.execute(
            INSERT_PRODUCT_DATA,
            (product_request.product_data.name, product_request.product_data.description,
             product_request.product_data.approved, product_request.product_data.image_file_path)
        )
        product_request.product_data.id = self.cursor.lastrowid
        await self.cursor.execute(
            INSERT_ADD_PRODUCT_REQUEST,
            (product_request.seller_id.id, None, None, product_request.product_data.id,
                product_request.request_status.value, None)
        )
        product_request.id = self.cursor.lastrowid
        return product_request

    async def create_product(self, product: ProductWithShopIdAndCategoriesIds) -> bool:
        product = product.copy()
        await self.cursor.execute(
            INSERT_PRODUCT,
            (product.price.amount, product.product_data.id, product.shop_id)
        )
        product.id = self.cursor.lastrowid

        await self.cursor.executemany(
            INSERT_PRODUCT_CATEGORIES,
            [(product.id, category_id) for category_id in product.categories_ids]
        )
        return True

    async def get_current_product_request(self, product_request_id: int) -> ProductCreationRequest:
        pass

    async def get_all_product_requests(self, shop: Shop) -> list[ProductCreationRequest]:
        pass

    async def update_product_request(self, product_request: ProductCreationRequest) -> ProductCreationRequest:
        pass

    async def get_product_request_satus(self, product_request: ProductCreationRequest) -> RequestStatus:
        pass
