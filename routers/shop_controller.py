from typing import Annotated
from fastapi import APIRouter, Form, Depends, Request

from domain.shop import Shop
from utils.templates import render
from dependencies.auth import get_user, require_auth, require_role
from domain.user import User, UserRole

router = APIRouter()


@router.post("/createShop", name="createShop",
             dependencies=[Depends(require_auth), Depends(require_role(UserRole.SELLER))])
async def create_shop(request: Request, seller: User = Depends(get_user)):
    return render(request, "seller/create_shop.html", {})


@router.get("/loadShopForm", name="loadShopForm",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.SELLER))])
async def load_shop_form(request: Request, seller: User = Depends(get_user)):
    return render(request, "seller/create_shop.html", {})
    # check if seller has already created shop


@router.get("/loadShop", name="loadShop",
            dependencies=[Depends(require_auth), Depends(require_role(UserRole.SELLER))])
async def load_created_shop(request: Request, seller: User = Depends(get_user)):
    return render(request, "seller/load_shop.html", {})

