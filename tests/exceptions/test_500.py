def test_error_interno(client):
    response = client.get("/forzar-error")  # Deben crear una ruta que falle a propósito

    assert response.status_code == 500
    assert b"Error interno" in response.data or b"500" in response.data
