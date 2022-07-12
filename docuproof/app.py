from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json

from docuproof.api.views import bp as APIBlueprint

application = Sanic("docuproof")
application.blueprint(APIBlueprint)


@application.route("/health")
async def health(request: Request) -> HTTPResponse:
    return json({"status": "ok"})
