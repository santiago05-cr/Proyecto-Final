from fastapi import status

def test_crear_registro_mental_health(client):
    response = client.post(
        "/mental_health/upload",
        data={
            "age": 22,
            "gender": "F",
            "feel_after": "Relaxed",
            "mental_harm": "None"
        },
        files={"image_file": ("test.jpg", b"fake-image", "image/jpeg")}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.json()


def test_crear_registro_videogame(client):
    response = client.post(
        "/videogames/upload",
        data={
            "age": 20,
            "gender": "M",
            "playing_hours": 5,
            "productive_time": 2
        },
        files={"image_file": ("test.jpg", b"fake-image", "image/jpeg")}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.json()
