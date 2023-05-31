from fastapi import Request
from fastapi.responses import RedirectResponse
from .router import router
from urllib.parse import quote_plus
from app import app


async def process_unauthorized_error(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 401:
        response = RedirectResponse(url=f"{router.url_path_for('login')}?next={quote_plus(str(request.url))}",
                                    status_code=302)
    return response


async def process_forbidden_error(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 403:
        # TODO: Redirect to a forbidden page
        response = RedirectResponse(url=app.url_path_for("catalog"), status_code=302)
    return response
