from io import BytesIO

def fake_image():
    return ("test.jpg", BytesIO(b"fake data"), "image/jpeg")


def test_actualizar_registro(client):
    # Crear registro inicial
    create = client.post(
        "/mental_health/upload",
        files={"image_file": fake_image()},
        data={
            "age": 15,
            "gender": "F",
            "feel_after": "sad",
            "mental_harm": "medium"
        }
    )

    data = create.json()
    record_id = data["id"]

    # Actualizar registro
    response = client.put(
        f"/mental_health/{record_id}",
        data={"age": 30, "feel_after": "better"}
    )

    assert response.status_code == 200
    assert response.json()["age"] == 30
    assert response.json()["feel_after"] == "better"
