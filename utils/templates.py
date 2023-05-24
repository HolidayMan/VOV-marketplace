from starlette.responses import Response
from starlette.requests import Request

from settings import TEMPLATE_RENDERER


def render(request: Request, template_name: str, context: dict) -> Response:
    context.update({"request": request})
    return TEMPLATE_RENDERER.TemplateResponse(template_name, context)


def render_to_string(template_name: str, context: dict) -> str:
    return TEMPLATE_RENDERER.get_template(template_name).render(context)
