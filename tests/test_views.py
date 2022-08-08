from docuproof.app import application


def test_index() -> None:
    _, response = application.test_client.get("/")
    assert response.status == 200
    assert response.content_type == "text/html; charset=utf-8"
