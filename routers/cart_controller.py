from fastapi import APIRouter, Request, Depends, HTTPException
from dependencies.auth import fake_get_user_with_custom_role
from domain.product import Product
from domain.user import User, UserRole
from services.cart_service import CartService
from utils.templates import render

router = APIRouter()
service = CartService()


@router.get("/cart/")
async def get_cart_items(request: Request, user: User = Depends(fake_get_user_with_custom_role(UserRole.CUSTOMER))):
    try:
        items = service.get_cart_items(user)
        return render(request, "cart.html",
               {"items_list": items})
    except Exception:
        raise HTTPException(status_code=401, detail="User not authorized")
        # TODO: Replace with redirection to the auth page


@router.post("/addToCart")
async def add_product(request: Request, product: Product, count: int, user: User = Depends(fake_get_user_with_custom_role(UserRole.CUSTOMER))):
    pass


