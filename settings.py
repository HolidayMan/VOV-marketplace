import os
from storages.FileSystemStorage import FileSystemStorage
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_FILE_STORAGE = FileSystemStorage(MEDIA_ROOT)
DEFAULT_STATICFILES_STORAGE = FileSystemStorage(os.path.join(BASE_DIR, STATIC_ROOT))

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATE_RENDERER = Jinja2Templates(directory=TEMPLATES_DIR)
