import os
from storages.FileSystemStorage import FileSystemStorage
from fastapi.templating import Jinja2Templates
from utils import filters

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.getenv('SECRET_KEY', 'ea105133356aba1911d75882b519fa220ba67e104bfe14775112ac4c33d7dda3')
HASHING_ALGORITHM = os.getenv('HASHING_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

CRYPT_CONTEXT_SCHEMES = ['bcrypt']

# Database
DB_SETTINGS = {
    "host": os.getenv('DB_HOST', 'localhost'),
    "port": os.getenv('DB_PORT', 3306),
    "db": os.getenv('DB_NAME', 'vov_database'),
    "user": os.getenv('DB_USER', 'vov_user'),
    "password": os.getenv('DB_PASSWORD', 'zCRkKF9DMJ'),
}
