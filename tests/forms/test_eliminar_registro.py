def test_eliminar_registro(client):
    # Crear un registro primero
    client.post("/crear", data={"nombre": "A", "descripcion": "B"})

    # Luego eliminar
    response = client.post("/eliminar/1", follow_redirects=True)

    assert response.status_code == 200
    assert b"eliminado" in response.data.lower() or b"exito" in response.data.lower()
