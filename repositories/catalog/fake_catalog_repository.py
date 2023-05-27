from money import Money
from repositories.catalog.catalog_repository import CatalogRepository
from domain.product import Category, Product, ProductData


class FakeCatalogRepository(CatalogRepository):
    products_food = [
        Product(
            price=Money(5, "USD"),
            id=1,
            shop_id=1,
            product_data=ProductData(**{
                "id": 1,
                "name": "Apple",
                "description": "Very tasty",
                "image_file_path": "/apple.jpg",
                "approved": True
            })
        )
    ]

    products_tools = [
        Product(
            price=Money(15, "USD"),
            id=2,
            shop_id=2,
            product_data=ProductData(**{
                "id": 2,
                "name": "Screwdriver",
                "description": "Very screw",
                "image_file_path":  "/screwdriver.png",
                "approved": True
            })
        )
    ]

    categories = [
        Category(**{
            "id": 1,
            "name": "tools"
        }),
        Category(**{
            "id": 2,
            "name": "food"
        })
    ]

    def get_catalog_items(self) -> list[Product]:
        return self.products_food + self.products_tools

    def get_catalog_items_with_category(self, category_name: str) -> list[Product]:
        if category_name == "tools":
            return self.products_tools
        if category_name == "food":
            return self.products_food

    def get_categories(self) -> list[Category]:
        return self.categories
