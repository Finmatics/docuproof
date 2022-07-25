from dotenv import load_dotenv
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json
from tortoise.contrib.sanic import register_tortoise

from docuproof.api.views import bp as APIBlueprint
from docuproof.blockchain import DocuProofContract
from docuproof.config import Config
from docuproof.ipfs import IPFSClient
from docuproof.tasks import TASK_LIST

load_dotenv()

application = Sanic("docuproof")
application.blueprint(APIBlueprint)
for task_func in TASK_LIST:
    application.add_task(task_func)

register_tortoise(application, config=Config.DATABASE_CONFIG, generate_schemas=True)


@application.route("/health")
async def health(request: Request) -> HTTPResponse:
    return json({"status": "ok"})


@application.before_server_start
async def before_start(app: Sanic) -> None:
    # Initialize connection with contract as soon as possible
    await DocuProofContract().connect()


@application.after_server_start
async def after_start(app: Sanic) -> None:
    # Initialize IPFS connection as soon as possible, but after the server is loaded
    IPFSClient()


@application.after_server_stop
async def after_stop(app: Sanic) -> None:
    # Close the IPFS connection
    IPFSClient().close()
