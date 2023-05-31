from fastapi import APIRouter, Depends, HTTPException, status, Request

from auth.dependencies import get_current_user
from auth.models import UserInDB
from domain.request import RequestStatus, ShopCreationRequest, ProductCreationRequest
from dependencies.auth import require_auth, require_role
from domain.user import User, UserRole
from services.catalog_service import CatalogService
from services.product_management.services import ProductManagementService
from services.uow.catalog.catalog_unit_of_work import MySQLAsyncCatalogUnitOfWork
from services.product_management.forms import ProductCreateForm
from services.uow.seller_product import MySQLAsyncProductCreationRequestUnitOfWork
from utils.templates import render

router = APIRouter(prefix='/product-management')

# TODO: make a different service for getting categories. For now it violates SRP
catalog_service = CatalogService(MySQLAsyncCatalogUnitOfWork())
products_management_service = ProductManagementService(MySQLAsyncProductCreationRequestUnitOfWork())


@router.get('/create-product', name='create-product', dependencies=[Depends(require_auth),
                                                                    Depends(require_role(UserRole.SELLER))])
async def create_product(request: Request):
    categories = await catalog_service.get_categories()
    return render(request, 'seller/create_product.html', {'categories': categories})


@router.post('/create-product', name='process-create-product', dependencies=[Depends(require_auth),
                                                                             Depends(require_role(UserRole.SELLER))])
async def process_create_product(request: Request, seller: UserInDB | None = Depends(get_current_user)):
    form = ProductCreateForm(request)
    await form.load_data()
    if form.is_valid():
        await products_management_service.create_product(form.get_data(), seller)
        return render(request, 'seller/create_product.html', {'success': True})

    return render(request, 'seller/create_product.html', {'form': form})
