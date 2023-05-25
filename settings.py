import os
from storages.FileSystemStorage import FileSystemStorage
from fastapi.templating import Jinja2Templates
from utils import filters

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_FILE_STORAGE = FileSystemStorage(MEDIA_ROOT, MEDIA_URL)
DEFAULT_STATICFILES_STORAGE = FileSystemStorage(STATIC_ROOT, STATIC_URL)

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATE_RENDERER = Jinja2Templates(directory=TEMPLATES_DIR)
filters.init_all_filters(TEMPLATE_RENDERER.env)

# TEMPLATE_RENDERER.env.add_extension('utils.tags.StaticExtension')
