from abc import ABC, abstractmethod

from domain.product import ProductData
from domain.request import ProductCreationRequest, RequestStatus
from repositories.exceptions import DoesNotExistError
from .sql import SELECT_OPEN_PRODUCT_REQUESTS, DECLINE_PRODUCT_REQUEST


class ProductCreationRequestWithoutUsers(ProductCreationRequest):
    seller_id: None = None
    moderator_id: None = None


class AsyncProductRequestApprovalRepository(ABC):

    @abstractmethod
    async def get_all_product_requests(self) -> list[ProductCreationRequestWithoutUsers]:
        pass

    @abstractmethod
    async def decline_product_request(self, product_data_id: int, refuse_reason: str, moderator_id: int) -> None:
        pass


class MySQLAsyncProductRequestApprovalRepository(AsyncProductRequestApprovalRepository):
    def __init__(self, cursor):
        self.cursor = cursor

    async def get_all_product_requests(self) -> list[ProductCreationRequestWithoutUsers]:
        await self.cursor.execute(
            SELECT_OPEN_PRODUCT_REQUESTS
        )
        rows = await self.cursor.fetchall()
        return [
            ProductCreationRequestWithoutUsers(
                request_status=RequestStatus(row['request_status_name']),
                refuse_reason=row['refuse_reason'],
                creation_date=row['creation_date'],
                check_date=row['check_date'],
                product_data=ProductData(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    image_file_path=row['image_file_path'],
                    approved=row['approved']
                )
            ) for row in rows
        ]

    async def decline_product_request(self, product_data_id: int, refuse_reason: str, moderator_id: int) -> None:
        await self.cursor.execute(
            DECLINE_PRODUCT_REQUEST,
            (refuse_reason, moderator_id, product_data_id, product_data_id)
        )

