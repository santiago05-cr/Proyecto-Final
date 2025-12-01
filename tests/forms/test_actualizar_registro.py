def test_actualizar_registro(client):
    # Primero crear registro
    client.post("/crear", data={"nombre": "A", "descripcion": "B"})

    # Luego actualizar
    update_data = {
        "nombre": "Actualizado",
        "descripcion": "Modificado"
    }

    response = client.post("/actualizar/1", data=update_data, follow_redirects=True)

    assert response.status_code == 200
    assert b"actualizado" in response.data.lower() or b"exito" in response.data.lower()
