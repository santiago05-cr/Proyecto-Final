import pytest
from main import app

@pytest.fixture
def client():
    return app.test_client()

def test_actualizacion_registro(client):
    payload = {
        "id": 1,
        "titulo": "Juego Editado",
        "anio": 2023
    }
    response = client.put("/videogame/update", json=payload)

    assert response.status_code in [200, 404]
