from fastapi.testclient import TestClient

from app.main import app


def test_inicio_redirige_a_materias():
    client = TestClient(app)

    respuesta = client.get("/", follow_redirects=False)

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/materias"
