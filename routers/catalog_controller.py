from fastapi import APIRouter, Request
from repositories.catalog.fake_catalog_repository import FakeAsyncCatalogRepository
from services.catalog_service import CatalogService
from services.exceptions import DataAccessError
from services.uow.catalog.catalog_unit_of_work import MySQLAsyncCatalogUnitOfWork
from utils.templates import render

router = APIRouter()
catalog_service = CatalogService(MySQLAsyncCatalogUnitOfWork())


@router.get("/catalog/", name="catalog")
async def load_catalog(request: Request, category: str | None = None):
    try:
        products = await catalog_service.get_catalog_items(category)
        categories = await catalog_service.get_categories()
        return render(request, "customer/catalog.html",
                      {"products_list": products, "category_list": categories})
    except DataAccessError:
        return render(request, "data_access_error.html", {})


