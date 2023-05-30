from typing import Annotated
from fastapi import APIRouter, Form, Depends, Request

from domain.shop import Shop
from services.shop_service import ShopService
from services.uow.shop.shop_unit_of_work import MySQLAsyncShopUnitOfWork
from utils.templates import render
from dependencies.auth import get_user, require_auth, require_role
from domain.user import User, UserRole

router = APIRouter()
service = ShopService(MySQLAsyncShopUnitOfWork())


@router.post("/createShop", name="createShop",
             dependencies=[Depends(require_auth), Depends(require_role(UserRole.SELLER))])
async def create_shop(request: Request, seller: User = Depends(get_user)):
    await service.create_shop("Vov", "Hiiiiii", seller)
    return render(request, "seller/create_shop.html", {})


@router.get("/loadShopForm", name="loadShopForm",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.SELLER))])
async def load_shop_form(request: Request, seller: User = Depends(get_user)):
    return render(request, "seller/create_shop.html", {})
    # TODO check if seller has already created shop


@router.get("/loadShop", name="loadShop",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.SELLER))])
async def load_created_shop(request: Request, seller: User = Depends(get_user)):
    return render(request, "seller/load_shop.html", {})
