from typing import Annotated
from fastapi import APIRouter, Form, Depends

from dependencies.auth import fake_get_user_with_custom_role
from domain.user import User, UserRole

router = APIRouter()


@router.post("/createShop")
async def create_shop(name: Annotated[str, Form()], description: Annotated[str, Form()],
                user: User = Depends(fake_get_user_with_custom_role(UserRole.SELLER))):
    pass


@router.get("/loadShop")
async def load_created_shop(user: User = Depends(fake_get_user_with_custom_role(UserRole.SELLER))):
    pass

