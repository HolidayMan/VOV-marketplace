from aiomysql import DictCursor
from pydantic import PositiveInt

from domain.request import RequestStatus
from domain.shop import ShopData
from domain.user import User
from repositories.moderator_shop_request_repository.exceptions import ShopRequestDoesNotExistError
from repositories.moderator_shop_request_repository.moderator_shop_request_repository import \
    AsyncModeratorShopRequestRepository
from repositories.moderator_shop_request_repository.sql import GET_SHOP_REQUESTS_LIST, GET_SHOP_REQUEST, \
    UPDATE_SHOP_REQUEST_STATUS_BY_SHOP_DATA_ID
from repositories.seller_shop_request_repository.shop_creation_request import ShopCreationRequestInDB


def map_row_to_shop_request(row) -> ShopCreationRequestInDB:
    shop_request_in_db = ShopCreationRequestInDB(
        seller_id=PositiveInt(row['seller_id']),
        request_status=RequestStatus(row['status_name']),
        refuse_reason=row['refuse_reason'],
        creation_date=row['creation_date'],
        check_date=row['check_date'],
        shop_data=ShopData(
            id=PositiveInt(row['shop_data_id']),
            name=row['shop_name'],
            description=row['description'],
            approved=row['approved']
        )
    )
    return shop_request_in_db


def map_rows_to_shop_requests_list(shop_requests_rows) -> list[ShopCreationRequestInDB]:
    shop_requests_list = []
    for row in shop_requests_rows:
        shop_request = map_row_to_shop_request(row)
        shop_requests_list.append(shop_request)
    return shop_requests_list


class MYSQLAsyncModeratorShopRequestRepository(AsyncModeratorShopRequestRepository):

    def __init__(self, cursor: DictCursor):
        self.cursor = cursor

    async def get_shop_requests_list(self) -> list[ShopCreationRequestInDB]:
        await self.cursor.execute(
            GET_SHOP_REQUESTS_LIST
        )
        if shop_requests_rows := await self.cursor.fetchall():
            shop_requests_list = map_rows_to_shop_requests_list(shop_requests_rows)
            return shop_requests_list
        return []

    async def get_shop_request(self, shop_data_id: PositiveInt) -> ShopCreationRequestInDB:
        await self.cursor.execute(GET_SHOP_REQUEST, (shop_data_id,))
        if shop_request_row := await self.cursor.fetchone():
            shop_request = map_row_to_shop_request(shop_request_row)
            return shop_request
        raise ShopRequestDoesNotExistError("Shop request does not exist")

    async def update_shop_request_status(self, shop_request: ShopCreationRequestInDB) -> ShopCreationRequestInDB:
        await self.cursor.execute(
            UPDATE_SHOP_REQUEST_STATUS_BY_SHOP_DATA_ID,
            (shop_request.refuse_reason,
             shop_request.request_status.name,
             shop_request.check_date,
             shop_request.shop_data.id)
        )
        return await self.get_shop_request(shop_request.shop_data.id)
