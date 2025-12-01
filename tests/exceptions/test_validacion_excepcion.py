def test_validacion_incorrecta(client):
    data = {}  # Enviar datos vacíos para provocar error

    response = client.post("/crear", data=data)

    assert response.status_code in (400, 422)
    assert b"Error" in response.data or b"Datos inválidos" in response.data
