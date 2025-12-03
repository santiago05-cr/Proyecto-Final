def test_404(client):
    response = client.get("/ruta/que/no/existe")
    assert response.status_code == 404
