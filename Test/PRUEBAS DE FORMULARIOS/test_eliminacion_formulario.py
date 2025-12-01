import pytest
from main import app

@pytest.fixture
def client():
    return app.test_client()

def test_eliminacion_registro(client):
    payload = {"id": 1}
    response = client.delete("/videogame/delete", json=payload)

    assert response.status_code in [200, 404]
