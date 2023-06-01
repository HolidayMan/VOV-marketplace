from datetime import datetime

from pydantic import PositiveInt
from starlette.datastructures import UploadFile

from auth.models import UserInDB
from domain.product import ProductData, ProductWithCategories, Product
from domain.request import ProductCreationRequest, RequestStatus
from repositories.exceptions import DoesNotExistError
from repositories.seller_products.create_product_request import ProductWithShopIdAndCategoriesIds
from services.exceptions import ProductDoesNotExistError
from services.product_management.exceptions import NotOwnerError
from services.uow.seller_product import AsyncProductManagementUnitOfWork
from settings import DEFAULT_FILE_STORAGE
from utils.images import get_product_image_name


class ProductManagementService:
    def __init__(self, uow: AsyncProductManagementUnitOfWork, file_storage=DEFAULT_FILE_STORAGE):
        self.uow = uow
        self.file_storage = file_storage

    async def save_product_image(self, upload_file: UploadFile) -> str:
        contents = await upload_file.read()
        file_path = f"products/{get_product_image_name(upload_file.filename)}"
        self.file_storage.save(file_path, contents)
        return file_path

    async def create_product(self, data: dict, seller: UserInDB):
        image_file_path = await self.save_product_image(data['image_data'])
        async with self.uow:
            add_product_request = await self.uow.products.create_product_request(ProductCreationRequest(
                seller_id=seller,
                request_status=RequestStatus.IN_PROCESS,
                creation_date=datetime.now(),
                product_data=ProductData(
                    name=data['name'],
                    description=data['description'],
                    image_file_path=image_file_path,
                    approved=False
                )
            ))
            await self.uow.products.create_product(ProductWithShopIdAndCategoriesIds(
                price=data['price'],
                shop_id=seller.id,
                product_data=add_product_request.product_data,
                categories_ids=data['categories']
            ))
            await self.uow.commit()

    async def get_products(self, seller: UserInDB) -> list[tuple[Product, RequestStatus]]:
        async with self.uow:
            return await self.uow.products.get_products_by_seller_id(seller.id)

    async def get_product(self, product_id: int, seller: UserInDB) -> tuple[ProductWithCategories, RequestStatus]:
        async with self.uow:
            try:
                product, status, seller_id = await self.uow.products.get_product_by_id(product_id)
            except DoesNotExistError:
                raise ProductDoesNotExistError("Product does not exist")
            if seller_id != seller.id:
                raise NotOwnerError("Seller is not owner of this product")
            return product, status
