import os

import pytest
from pytest import FixtureRequest
from tortoise.contrib.test import finalizer, initializer


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request: FixtureRequest) -> None:
    db_url = os.environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    initializer(["docuproof.models"], db_url=db_url, app_label="models")
    request.addfinalizer(finalizer)
