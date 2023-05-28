from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from pydantic import PositiveInt

from dependencies.auth import get_user, require_auth, require_role
from domain.user import User, UserRole
from repositories.cart.fake_cart_repository import FAKE_CART_REPO
from services.cart_service import CartService
from utils.templates import render

router = APIRouter()
service = CartService(FAKE_CART_REPO)


@router.get("/cart/", name="cart", dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def get_cart_items(request: Request, user: User = Depends(get_user)):
    try:
        items = service.get_cart_items(user)
        return render(request, "cart.html",
               {"items_list": items})
    except Exception:
        raise HTTPException(status_code=401, detail="User not authorized")
        # TODO: Replace with redirection to the auth page


@router.post("/addToCart", name="addToCart", dependencies=[Depends(require_auth), Depends(require_role(UserRole.CUSTOMER))])
async def add_product(productId: Annotated[PositiveInt, Form()], count: Annotated[PositiveInt, Form()],
                      user: User = Depends(get_user)):
    pass


@router.delete("/removeItemFromCart/", name="removeItemFromCart", dependencies=[Depends(require_auth),
                                                                                Depends(require_role(UserRole.CUSTOMER))])
async def remove_item(itemId: Annotated[PositiveInt, Form()], user: User = Depends(get_user)):
    pass


