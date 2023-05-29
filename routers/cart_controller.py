from typing import Annotated
from fastapi import APIRouter, Request, Depends, Form
from pydantic import PositiveInt
from dependencies.auth import get_user, require_auth, require_role
from domain.user import User, UserRole
from services.cart_service import CartService
from services.exceptions import DataAccessError
from services.uow.cart.cart_unit_of_work import MySQLAsyncCartUnitOfWork
from utils.templates import render

router = APIRouter()
service = CartService(MySQLAsyncCartUnitOfWork())


@router.get("/cart/", name="cart", dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def get_cart_items(request: Request, user: User = Depends(get_user)):
    try:
        items = await service.get_cart_items(user)
        return render(request, "customer/cart.html",
                      {"items_list": items})
    except DataAccessError:
        return {"something": "went wrong"}
    # TODO: Render some error page if there is database error


@router.post("/addToCart", name="addToCart",
             dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def add_product(productId: Annotated[PositiveInt, Form()], count: Annotated[PositiveInt, Form()],
                      user: User = Depends(get_user)):
    pass

@router.delete("/removeItemFromCart/", name="removeItemFromCart", dependencies=[Depends(require_auth),
                                                                                Depends(
                                                                                    require_role(UserRole.CUSTOMER))])
async def remove_item(itemId: Annotated[PositiveInt, Form()], user: User = Depends(get_user)):
    pass
