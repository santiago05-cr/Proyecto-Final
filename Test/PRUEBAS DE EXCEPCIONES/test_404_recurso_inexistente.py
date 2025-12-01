import pytest
from main import app

@pytest.fixture
def client():
    return app.test_client()

def test_ruta_no_existe(client):
    response = client.get("/ruta-que-no-existe")
    assert response.status_code == 404
