def test_500_error_simulado(client):
    # Este test solo verifica que NO crashee tu servidor
    response = client.put("/mental_health/invalid-id", data={})
    assert response.status_code in (400, 422, 500)
