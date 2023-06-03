from pydantic import PositiveInt

from db import AsyncSession
from domain.request import RequestStatus
from domain.shop import ShopData
from domain.user import User
from repositories.seller_shop_request_repository.seller_shop_request_repository import AsyncSellerShopRequestRepository
from repositories.seller_shop_request_repository.shop_creation_request import ShopCreationRequestInDB
from repositories.seller_shop_request_repository.sql import CREATE_SHOP_REQUEST, GET_SHOP_REQUESTS


def map_row_to_creation_request(row) -> ShopCreationRequestInDB:
    shop_creation_request_in_db = ShopCreationRequestInDB(
        seller_id=PositiveInt(row['seller_id']),
        request_status=RequestStatus(row['status_name']),
        refuse_reason=row['refuse_reason'],
        creation_date=row['creation_date'],
        check_date=row['check_date'],
        shop_data=ShopData(
            name=row['shop_name'],
            description=row['description'],
            approved=row['approved']
        )
    )
    return shop_creation_request_in_db


def map_rows_to_shop_requests_list(shop_requests_rows) -> list[ShopCreationRequestInDB]:
    shop_requests_list = []
    for row in shop_requests_rows:
        shop_request = map_row_to_creation_request(row)
        shop_requests_list.append(shop_request)
    return shop_requests_list


class MySQLAsyncSellerShopRequestRepository(AsyncSellerShopRequestRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_shop_request(self, shop_request: ShopCreationRequestInDB) -> ShopCreationRequestInDB:
        async with self.session.cursor() as cursor:
            shop_request_values = (shop_request.shop_data.id,
                                   shop_request.request_status.name,
                                   shop_request.creation_date,
                                   shop_request.seller_id)
            await cursor.execute(CREATE_SHOP_REQUEST, shop_request_values)
            await self.session.commit()
        return shop_request

    async def get_all_shop_requests(self, seller: User) -> list[ShopCreationRequestInDB]:
        async with self.session.cursor() as cursor:
            await cursor.execute(GET_SHOP_REQUESTS, seller)

            if shop_request_rows := await cursor.fetchall():
                shop_request_lists = map_rows_to_shop_requests_list(shop_request_rows)
                return shop_request_lists
        return []

