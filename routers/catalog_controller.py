from fastapi import APIRouter, Request
from utils.templates import render

router = APIRouter()


@router.get("/catalog")
async def load_catalog(request: Request):
        return render(request, "catalog.html",
                      {"some_variable": "test"})
