from domain.request import ProductCreationRequest
from domain.user import User
from repositories.moderator_products.product_request_approval_repository import ProductCreationRequestWithoutUsers
from services.uow.moderator_product import AsyncModeratorProductUnitOfWork


class ModeratorProductService:
    def __init__(self, uow: AsyncModeratorProductUnitOfWork):
        self._uow = uow

    async def get_product_request(self, id_: int):
        async with self._uow:
            return await self._uow.requests.get_product_request(id_)

    async def get_product_requests(self) -> list[ProductCreationRequestWithoutUsers]:
        async with self._uow:
            return await self._uow.requests.get_all_product_requests()

    async def decline_product_request(self, product_data_id: int, refuse_reason: str, moderator: User) -> None:
        async with self._uow:
            await self._uow.requests.decline_product_request(product_data_id, refuse_reason, moderator.id)
            await self._uow.commit()
