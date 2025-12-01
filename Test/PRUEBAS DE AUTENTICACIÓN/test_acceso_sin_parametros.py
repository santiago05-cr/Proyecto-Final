import pytest
from main import app

@pytest.fixture
def client():
    return app.test_client()

def test_acceso_sin_parametros(client):
    response = client.get("/mental-health")
    assert response.status_code == 400 or response.status_code == 422
