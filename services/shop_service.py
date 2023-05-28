from domain.user import User
from repositories.shop.shop_repository import ShopRepository
from repositories.shop.shop_request_repository import ShopRequestRepository


class ShopService:
    _repository: ShopRepository
    _repository: ShopRequestRepository

    def __init__(self, shop_repository: ShopRepository):
        self.shopRepository = shop_repository

    def create_shop(self, name: str, description: str, seller: User):
        pass

    def get_shop(self, seller: User):
        pass

    def get_shop_creation_request(self, seller: User):
        pass


