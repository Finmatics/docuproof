from pytest import MonkeyPatch

from docuproof.config import Config


def test_index(monkeypatch: MonkeyPatch) -> None:
    with monkeypatch.context() as m:
        m.setattr(Config, "SHOW_FRONTEND", True)
        m.setattr(Config, "RUN_BACKGROUND_TASKS", False)

        from docuproof.app import application

        _, response = application.test_client.get("/")
        assert response.status == 200
        assert response.content_type == "text/html; charset=utf-8"
