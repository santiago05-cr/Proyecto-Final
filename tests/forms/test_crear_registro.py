def test_crear_registro(client):
    data = {
        "nombre": "Prueba",
        "descripcion": "Registro de prueba"
    }

    response = client.post("/crear", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b"creado" in response.data.lower() or b"exito" in response.data.lower()
