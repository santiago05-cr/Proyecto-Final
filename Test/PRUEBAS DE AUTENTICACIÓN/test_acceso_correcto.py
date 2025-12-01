import pytest
from main import app

@pytest.fixture
def client():
    return app.test_client()

def test_acceso_correcto(client):
    response = client.get("/mental-health?user=test")
    assert response.status_code == 200
