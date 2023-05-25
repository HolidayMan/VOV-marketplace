from jinja2.ext import Extension
from jinja2.nodes import Const, Node, CallBlock, Output

from settings import DEFAULT_STATICFILES_STORAGE


# this still doesn't work
class StaticExtension(Extension):
    tags = {'static'}

    def _render_tag(self, path: str) -> str:
        return DEFAULT_STATICFILES_STORAGE.url(path)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args: Const = parser.parse_expression()
        call = self.call_method('_render_tag', [args.value], lineno=lineno)
        to_return = Output([call], lineno=lineno)
        return to_return
