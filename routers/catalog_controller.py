from fastapi import APIRouter, Request
from repositories.catalog.fake_catalog_repository import FakeCatalogRepository
from services.catalog_service import CatalogService
from utils.templates import render

router = APIRouter()
catalog_service = CatalogService(FakeCatalogRepository())


@router.get("/catalog/", name="catalog")
async def load_catalog(request: Request, category: str | None = None):
    products = catalog_service.get_catalog_items(category)
    categories = catalog_service.get_categories()
    return render(request, "catalog.html",
                  {"products_list": products, "category_list": categories})

