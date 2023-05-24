from starlette.responses import Response

from settings import TEMPLATE_RENDERER


def render(template_name: str, context: dict) -> Response:
    return TEMPLATE_RENDERER.TemplateResponse(template_name, context)


def render_to_string(template_name: str, context: dict) -> str:
    return TEMPLATE_RENDERER.get_template(template_name).render(context)
