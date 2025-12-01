def test_ruta_inexistente(client):
    response = client.get("/ruta/que/no/existe")

    assert response.status_code == 404
    assert b"404" in response.data or b"No encontrado" in response.data
