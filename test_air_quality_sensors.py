from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_sensor():
    response = client.post("/api/air-quality-sensors/", json={
        "name": "Test Sensor",
        "location": "Pittsburgh",
        "latitude": 40.44,
        "longitude": -79.94,
        "pm25": 12.5,
        "aqi": 52,
        "status": "active"
    })
    return response


def test_create_sensor():
    response = create_sensor()
    assert response.status_code == 201
    assert response.json()["name"] == "Test Sensor"


def test_list_sensors():
    response = client.get("/api/air-quality-sensors/")
    assert response.status_code == 200
    assert "sensors" in response.json()


def test_get_sensor():
    sensor_id = create_sensor().json()["id"]
    response = client.get(f"/api/air-quality-sensors/{sensor_id}")
    assert response.status_code == 200
    assert response.json()["id"] == sensor_id


def test_update_sensor():
    sensor_id = create_sensor().json()["id"]
    response = client.put(f"/api/air-quality-sensors/{sensor_id}", json={"status": "offline"})
    assert response.status_code == 200
    assert response.json()["status"] == "offline"


def test_delete_sensor():
    sensor_id = create_sensor().json()["id"]
    response = client.delete(f"/api/air-quality-sensors/{sensor_id}")
    assert response.status_code == 204
    response = client.get(f"/api/air-quality-sensors/{sensor_id}")
    assert response.status_code == 404


def test_get_missing_sensor():
    response = client.get("/api/air-quality-sensors/99999")
    assert response.status_code == 404