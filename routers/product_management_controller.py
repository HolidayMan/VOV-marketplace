from fastapi import APIRouter, Depends, HTTPException, status, Request

from auth.dependencies import get_current_user
from auth.models import UserInDB
from dependencies.auth import require_auth, require_role
from domain.user import User, UserRole
from services.catalog_service import CatalogService
from services.exceptions import ProductDoesNotExistError
from services.product_management.exceptions import NotOwnerError
from services.product_management.services import ProductManagementService
from services.uow.catalog.catalog_unit_of_work import MySQLAsyncCatalogUnitOfWork
from services.product_management.forms import ProductCreateForm
from services.uow.seller_product import MySQLAsyncProductManagementUnitOfWork
from utils.templates import render

router = APIRouter(prefix='/product-management')

# TODO: make a different service for getting categories. For now it violates SRP
catalog_service = CatalogService(MySQLAsyncCatalogUnitOfWork())
products_management_service = ProductManagementService(MySQLAsyncProductManagementUnitOfWork())


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


@router.get('/my-products', name='my-products', dependencies=[Depends(require_auth),
                                                              Depends(require_role(UserRole.SELLER))])
async def my_products(request: Request, seller: UserInDB | None = Depends(get_current_user)):
    products = await products_management_service.get_products(seller)
    return render(request, 'seller/my_products.html', {'products': products})


@router.get('/my-products/{product_id}', name='my-product', dependencies=[Depends(require_auth),
                                                                          Depends(require_role(UserRole.SELLER))])
async def my_product(request: Request, product_id: int, seller: UserInDB = Depends(get_current_user)):
    # TODO: view refuse_reason if request was refused
    try:
        product, request_status = await products_management_service.get_product(product_id, seller)
    except NotOwnerError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    except ProductDoesNotExistError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return render(request, 'seller/my_product.html', {'product': product, 'request_status': request_status})
