from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json
from tortoise.contrib.sanic import register_tortoise

from docuproof.api.views import bp as APIBlueprint

application = Sanic("docuproof", env_prefix="DOCU_")
application.blueprint(APIBlueprint)

register_tortoise(
    application, db_url=application.config.DATABASE_URL, modules={"models": ["docuproof.models"]}, generate_schemas=True
)


@application.route("/health")
async def health(request: Request) -> HTTPResponse:
    return json({"status": "ok"})
