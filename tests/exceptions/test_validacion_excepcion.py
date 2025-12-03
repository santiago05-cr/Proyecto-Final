def test_validacion_formulario(client):
    response = client.post(
        "/login",
        data={"username": ""}  # falta username válido
    )

    assert response.status_code == 422
