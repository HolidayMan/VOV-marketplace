from money import Money
from pydantic import PositiveInt

from services.uow.seller_product import AsyncProductManagementUnitOfWork


class ProductCreateForm:
    def __init__(self, request):
        self.request = request
        self.price: str | None = None
        self.name: str | None = None
        self.description: str | None = None
        self.image_data: bytes | None = None
        self.categories: list[PositiveInt] | None = None
        self.errors = {}

    async def load_data(self):
        form = await self.request.form()
        self.price = form.get('price')
        self.name = form.get('name')
        self.description = form.get('description')
        self.image_data = form.get('image')
        self.categories = form.getlist('categories')

    def is_valid(self):
        try:
            Money(self.price, 'UAH')
        except ValueError:
            self.errors['price'] = 'Invalid price format. Must be a number. For example: 10.50'

        if not self.name:
            self.errors['name'] = 'Name is required'

        if not self.description:
            self.errors['description'] = 'Description is required'

        if not self.image_data:
            self.errors['image'] = 'Image is required'

        if not self.categories:
            self.errors['categories'] = 'Categories is required'

        return not self.errors

    def get_data(self):
        return {
            'price': Money(self.price, 'UAH'),
            'name': self.name,
            'description': self.description,
            'image_data': self.image_data,
            'categories': self.categories,
        }
