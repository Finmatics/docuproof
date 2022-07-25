from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json
from tortoise.contrib.sanic import register_tortoise

from docuproof.api.views import bp as APIBlueprint
from docuproof.config import Config
from docuproof.tasks import TASK_LIST

application = Sanic("docuproof")
application.blueprint(APIBlueprint)
for task_func in TASK_LIST:
    application.add_task(task_func)

register_tortoise(application, config=Config.DATABASE_CONFIG, generate_schemas=True)


@application.route("/health")
async def health(request: Request) -> HTTPResponse:
    return json({"status": "ok"})
