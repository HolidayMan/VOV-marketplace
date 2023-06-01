from abc import ABC, abstractmethod

from aiomysql import DictCursor
from money import Money
from pydantic.types import PositiveInt

from db import AsyncSession
from domain.product import Product, Category, ProductWithCategories, ProductData, Category
from domain.request import ProductCreationRequest, RequestStatus
from domain.shop import Shop
from .sql import INSERT_PRODUCT_DATA, INSERT_ADD_PRODUCT_REQUEST, INSERT_PRODUCT, INSERT_PRODUCT_CATEGORIES, \
    SELECT_PRODUCTS_BY_SELLER_ID, SELECT_PRODUCT_BY_ID
from ..exceptions import DoesNotExistError


class ProductWithShopId(Product):
    shop_id: PositiveInt


class ProductWithShopIdAndCategoriesIds(ProductWithShopId):
    categories_ids: list[PositiveInt]


class AsyncProductManagementRepository(ABC):

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

    @abstractmethod
    async def get_products_by_seller_id(self, seller_id: int) -> list[tuple[Product, RequestStatus]]:
        pass

    @abstractmethod
    async def get_product_by_id(self, product_id: int) -> tuple[ProductWithCategories, RequestStatus, PositiveInt]:
        pass


class MySQLAsyncProductManagementRepository(AsyncProductManagementRepository):
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

    async def get_products_by_seller_id(self, seller_id: int) -> list[tuple[Product, RequestStatus]]:
        await self.cursor.execute(SELECT_PRODUCTS_BY_SELLER_ID, (seller_id,))
        data = await self.cursor.fetchall()
        return [
            (Product(
                id=row['id'],
                price=Money(row['price'], 'UAH'),
                product_data=ProductData(
                    id=row['product_data_id'],
                    name=row['name'],
                    description=row['description'],
                    image_file_path=row['image_file_path'],
                    approved=row['approved']
                ),
            ), RequestStatus(row['request_status_name']))
            for row in data
        ]

    async def get_product_by_id(self, product_id: int) -> tuple[ProductWithCategories, RequestStatus, PositiveInt]:
        """Returns product, request status and shop id"""
        await self.cursor.execute(SELECT_PRODUCT_BY_ID, (product_id,))
        data = await self.cursor.fetchall()
        if not data:
            raise DoesNotExistError(f'Product with id {product_id} does not exist')
        product = None
        for row in data:
            if not product:
                product = ProductWithCategories(
                    id=row['id'],
                    price=Money(row['price'], 'UAH'),
                    product_data=ProductData(
                        id=row['product_data_id'],
                        name=row['name'],
                        description=row['description'],
                        image_file_path=row['image_file_path'],
                        approved=row['approved']
                    ),
                    categories=[]
                )
            product.categories.append(Category(
                id=row['category_id'],
                name=row['category_name']
            ))
        return product, RequestStatus(data[0]['request_status_name']), data[0]['seller_id']

    async def get_current_product_request(self, product_request_id: int) -> ProductCreationRequest:
        pass

    async def get_all_product_requests(self, shop: Shop) -> list[ProductCreationRequest]:
        pass

    async def update_product_request(self, product_request: ProductCreationRequest) -> ProductCreationRequest:
        pass

    async def get_product_request_satus(self, product_request: ProductCreationRequest) -> RequestStatus:
        pass
