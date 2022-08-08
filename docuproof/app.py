from dotenv import load_dotenv
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic_ext import render
from tortoise.contrib.sanic import register_tortoise

from docuproof.blockchain import DocuProofContract
from docuproof.config import Config
from docuproof.ipfs import IPFSClient
from docuproof.tasks import TASK_LIST
from docuproof.views import bp as APIBlueprint

load_dotenv()

application = Sanic("docuproof")

application.blueprint(APIBlueprint)

for task_func in TASK_LIST:
    application.add_task(task_func)

register_tortoise(application, config=Config.DATABASE_CONFIG, generate_schemas=True)


@application.route("/health")
async def health(request: Request) -> HTTPResponse:
    return json({"status": "ok"})


if Config.SHOW_FRONTEND:

    @application.route("/")
    async def index(request: Request) -> HTTPResponse:
        return await render(
            "index.html",
            environment=Config.TEMPLATE_ENVIRONMENT,
            context={"token": Config.PRIVATE_ENDPOINTS_TOKEN},
        )


@application.before_server_start
async def before_start(app: Sanic) -> None:
    # Initialize connection with contract as soon as possible
    await DocuProofContract().connect()


@application.after_server_start
async def after_start(app: Sanic) -> None:
    # Initialize IPFS connection as soon as possible, but after the server is loaded
    ipfs_addr = Config.IPFS_API_ENDPOINT if Config.IPFS_API_ENDPOINT else None
    ipfs_auth = (
        (Config.IPFS_ENDPOINT_USERNAME, Config.IPFS_ENDPOINT_PASSWORD)
        if Config.IPFS_ENDPOINT_USERNAME and Config.IPFS_ENDPOINT_PASSWORD
        else None
    )
    IPFSClient().connect(
        addr=ipfs_addr,
        auth=ipfs_auth,
    )


@application.after_server_stop
async def after_stop(app: Sanic) -> None:
    # Close the IPFS connection
    IPFSClient().close()
