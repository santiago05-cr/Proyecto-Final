import pytest
from main import app

@pytest.fixture
def client():
    return app.test_client()

def test_error_interno(client):
    payload = {"id": "no-es-numero"}  # Esto debería romper si el código no valida
    response = client.put("/videogame/update", json=payload)

    assert response.status_code in [400, 500]
