import pytest
from main import app

@pytest.fixture
def client():
    return app.test_client()

def test_creacion_registro(client):
    payload = {
        "titulo": "Nuevo Juego",
        "anio": 2024,
        "genero": "Acción"
    }
    response = client.post("/videogame/create", json=payload)

    assert response.status_code == 200
    assert "creado" in response.get_data(as_text=True).lower()
