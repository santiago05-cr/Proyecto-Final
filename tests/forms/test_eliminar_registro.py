from io import BytesIO

def fake_image():
    return ("test.jpg", BytesIO(b"fake data"), "image/jpeg")


def test_eliminar_registro(client):
    # Crear registro
    create = client.post(
        "/mental_health/upload",
        files={"image_file": fake_image()},
        data={
            "age": 22,
            "gender": "M",
            "feel_after": "fine",
            "mental_harm": "low"
        }
    )

    record_id = create.json()["id"]

    # Eliminar registro
    response = client.post(f"/mental_health/delete/{record_id}")

    assert response.status_code == 200
    assert "eliminado" in response.text.lower()
