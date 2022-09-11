import os
from copy import deepcopy

import pytest
from sanic import Sanic
from tortoise.contrib.sanic import register_tortoise

from docuproof.config import Config
from docuproof.views import bp as APIBlueprint
from docuproof.views import health


@pytest.fixture
def app() -> Sanic:
    config = deepcopy(Config.DATABASE_CONFIG)
    config["connections"]["default"] = os.environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")

    app = Sanic("docuproof-test")
    app.blueprint(APIBlueprint)
    app.add_route(health, "/health")

    register_tortoise(app, config=config, generate_schemas=True)

    return app


async def test_health(app: Sanic) -> None:
    _, response = await app.asgi_client.get("/health")
    assert response.status == 200
    assert response.json == {"status": "ok"}
