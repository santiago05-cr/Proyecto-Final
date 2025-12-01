import pytest
from main import app

@pytest.fixture
def client():
    return app.test_client()

def test_acceso_invalido(client):
    response = client.get("/mental-health?user=@@@")
    assert response.status_code in [400, 404]
