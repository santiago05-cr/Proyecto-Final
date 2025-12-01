import pytest
from main import app

@pytest.fixture
def client():
    return app.test_client()

def test_error_validacion(client):
    payload = {"titulo": ""}  # Datos inválidos
    response = client.post("/videogame/create", json=payload)

    assert response.status_code in [400, 422]
