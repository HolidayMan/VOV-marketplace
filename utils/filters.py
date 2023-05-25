import jinja2

import settings


def make_static_url(path: str) -> str:
    return settings.DEFAULT_STATICFILES_STORAGE.url(path)


def make_media_url(path: str) -> str:
    return settings.DEFAULT_FILE_STORAGE.url(path)


def init_all_filters(env: jinja2.Environment):
    env.filters.update(make_static=make_static_url)
    env.filters.update(make_media=make_media_url)
