from fastapi import APIRouter, Request
from repositories.fake_catalog_repository import FakeCatalogRepository
from services.catalog_service import CatalogService
from utils.templates import render

router = APIRouter()
catalog_service = CatalogService(FakeCatalogRepository())


@router.get("/catalog")
async def load_catalog(request: Request):
    products = catalog_service.get_catalog_items()
    return render(request, "catalog.html",
                  {"products_list": products})
