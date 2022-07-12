from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, text
from sanic.views import HTTPMethodView

bp = Blueprint("api", url_prefix="/api", version=1)


class HashView(HTTPMethodView):
    async def get(self, request: Request) -> HTTPResponse:
        return text("HashView")


class ProofView(HTTPMethodView):
    async def get(self, request: Request) -> HTTPResponse:
        return text("ProofView")


bp.add_route(HashView.as_view(), "/hash")
bp.add_route(ProofView.as_view(), "/proof")
