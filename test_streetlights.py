"""Street lights endpoint tests. Run: python -m pytest test_streetlights.py -v."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base, get_db
from main import app


@pytest.fixture
def client():
    """Use a fresh in-memory database so tests never change saved city records."""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    test_session = sessionmaker(bind=engine)

    def override_get_db():
        with test_session() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()


def create_streetlight_helper(client, **changes):
    """Create a sample street light, allowing different poles and filter values."""
    data = {
        "location": "Forbes Avenue, Pittsburgh",
        "pole_id": "PIT-001",
        "light_type": "LED",
        "wattage": 80,
        "installation_date": "2024-05-01",
        "last_maintenance": "2026-11-01",
        "is_operational": True,
        "energy_consumption_kwh": 28.8,
    }
    data.update(changes)
    response = client.post("/api/streetlights/", json=data)
    assert response.status_code == 201, response.text
    return response.json()


def test_create_streetlight(client):
    data = create_streetlight_helper(client)
    assert data["pole_id"] == "PIT-001"
    assert data["wattage"] == 80
    assert data["light_type"] == "LED"
    assert data["installation_date"] == "2024-05-01"
    assert data["last_maintenance"] == "2026-11-01"
    assert data["energy_consumption_kwh"] == 28.8
    assert data["is_operational"] is True
    assert data["id"] > 0
    assert data["created_at"] and data["updated_at"]


def test_create_with_only_required_fields(client):
    response = client.post("/api/streetlights/", json={
        "location": "Fifth Avenue", "pole_id": "PIT-002",
        "light_type": "Sodium", "wattage": 100,
    })
    assert response.status_code == 201
    assert response.json()["is_operational"] is True
    assert response.json()["installation_date"] is None


def test_list_streetlights(client):
    assert client.get("/api/streetlights/").json() == {"total": 0, "streetlights": []}
    created = create_streetlight_helper(client)
    response = client.get("/api/streetlights/")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["streetlights"][0]["id"] == created["id"]


def test_get_streetlight(client):
    created = create_streetlight_helper(client)
    response = client.get(f'/api/streetlights/{created["id"]}')
    assert response.status_code == 200
    assert response.json() == created


def test_update_streetlight(client):
    created = create_streetlight_helper(client)
    response = client.put(f'/api/streetlights/{created["id"]}', json={
        "is_operational": False, "wattage": 60, "light_type": "Halogen",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["is_operational"] is False
    assert data["wattage"] == 60
    assert data["light_type"] == "Halogen"
    assert data["location"] == created["location"]
    assert data["created_at"] == created["created_at"]
    assert client.get(f'/api/streetlights/{created["id"]}').json() == data


def test_clear_optional_fields(client):
    created = create_streetlight_helper(client)
    response = client.put(f'/api/streetlights/{created["id"]}', json={
        "installation_date": None, "last_maintenance": None, "energy_consumption_kwh": None,
    })
    assert response.status_code == 200
    for field in ("installation_date", "last_maintenance", "energy_consumption_kwh"):
        assert response.json()[field] is None


def test_delete_streetlight(client):
    created = create_streetlight_helper(client)
    response = client.delete(f'/api/streetlights/{created["id"]}')
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f'/api/streetlights/{created["id"]}').status_code == 404


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_nonexistent_streetlight(client, method):
    options = {"json": {"wattage": 70}} if method == "put" else {}
    response = getattr(client, method)("/api/streetlights/99999", **options)
    assert response.status_code == 404


def test_filter_search_and_pagination(client):
    first = create_streetlight_helper(client)
    second = create_streetlight_helper(client, pole_id="PIT-002", is_operational=False)
    create_streetlight_helper(client, pole_id="PIT-003", light_type="Sodium", location="Fifth Avenue")

    filtered = client.get("/api/streetlights/", params={"light_type": "LED"}).json()
    assert filtered["total"] == 2
    assert all(light["light_type"] == "LED" for light in filtered["streetlights"])
    for operational, expected in (("true", 2), ("false", 1)):
        result = client.get("/api/streetlights/", params={"is_operational": operational}).json()
        assert result["total"] == expected
        assert all(light["is_operational"] == (operational == "true") for light in result["streetlights"])

    searched = client.get("/api/streetlights/", params={"search": "FORBES"}).json()
    assert searched["total"] == 2
    combined = client.get("/api/streetlights/", params={
        "search": "forbes", "light_type": "LED", "is_operational": "false",
    }).json()
    assert combined["total"] == 1
    assert combined["streetlights"][0]["id"] == second["id"]

    page = client.get("/api/streetlights/", params={"skip": 1, "limit": 1}).json()
    assert page["total"] == 3
    assert [light["id"] for light in page["streetlights"]] == [second["id"]]
    assert first["id"] < second["id"]
    assert client.get("/api/streetlights/?search=unknown").json() == {"total": 0, "streetlights": []}


def test_duplicate_pole_id(client):
    first = create_streetlight_helper(client)
    response = client.post("/api/streetlights/", json={
        "location": "Another street", "pole_id": first["pole_id"],
        "light_type": "LED", "wattage": 50,
    })
    assert response.status_code == 409
    second = create_streetlight_helper(client, pole_id="PIT-002")
    response = client.put(f'/api/streetlights/{second["id"]}', json={"pole_id": first["pole_id"]})
    assert response.status_code == 409
    assert client.get(f'/api/streetlights/{second["id"]}').json()["pole_id"] == "PIT-002"
    assert client.get("/api/streetlights/").json()["total"] == 2


@pytest.mark.parametrize("changes", [
    {"location": "   "}, {"pole_id": ""}, {"light_type": "Neon"},
    {"wattage": 0}, {"wattage": -10}, {"wattage": 1.5},
    {"energy_consumption_kwh": -1}, {"installation_date": "not-a-date"},
])
def test_invalid_create(client, changes):
    data = {"location": "Forbes Avenue", "pole_id": "PIT-001", "light_type": "LED", "wattage": 80}
    data.update(changes)
    assert client.post("/api/streetlights/", json=data).status_code == 422
    assert client.get("/api/streetlights/").json()["total"] == 0


def test_missing_required_fields(client):
    assert client.post("/api/streetlights/", json={}).status_code == 422


@pytest.mark.parametrize("field", ["location", "pole_id", "light_type", "wattage", "is_operational"])
def test_update_cannot_null_required_fields(client, field):
    created = create_streetlight_helper(client)
    response = client.put(f'/api/streetlights/{created["id"]}', json={field: None})
    assert response.status_code == 422
    assert client.get(f'/api/streetlights/{created["id"]}').json() == created


@pytest.mark.parametrize("query", ["skip=-1", "limit=0", "limit=501", "light_type=Neon", "is_operational=invalid"])
def test_invalid_query(client, query):
    assert client.get(f"/api/streetlights/?{query}").status_code == 422


def test_router_documentation(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "post" in paths["/api/streetlights/"]
    assert "put" in paths["/api/streetlights/{streetlight_id}"]
    assert "/api/streetlights" in client.get("/").json()["endpoints"]
