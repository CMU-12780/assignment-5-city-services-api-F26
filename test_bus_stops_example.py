"""
Example test file for Bus Stops router
Use this as a reference for testing your own routers

To run tests:
1. Install pytest: pip install pytest httpx
2. Run: pytest test_bridges_example.py -v
"""
from fastapi.testclient import TestClient
from main import app
from datetime import date




client = TestClient(app)


def create_BusStops_helper(full_result=False):
    """Helper to create a new bridge"""
    response = client.post(
        "/api/bus_stops/",
        json={
            "bus_stop_id" : "STOP005",
            "location" : "Fifth Ave",
            "routes_served" : "71B, 71D",
            "has_shelter" : False,
            "has_bench" : True,
            "has_lighting" : False,
            "daily_boardings_avg" :240,
            "last_maintenance": date(2026,11,1).isoformat()
        }
    )
    if full_result:
        return response
    else:
        data = response.json()
        return data["id"]

def test_create_BusStop():
    """Test creating a new bridge"""
    response = create_BusStops_helper(full_result=True)
    assert response.status_code == 201
    data = response.json()
    assert data["has_shelter"] == False
    assert data["location"] == "Fifth Ave"
    assert "bus_stop_id" in data

def test_list_BusStops():
    """Test listing all bridges"""
    response = client.get("/api/bus_stops/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "bus_stops" in data
    assert isinstance(data["bus_stops"], list)


def test_get_BusStops():
    """Test getting a specific bus stop"""
    # First create a bus stop
    id = create_BusStops_helper()

    # Then retrieve it
    response = client.get(f"/api/bus_stops/{id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == id


def test_update_BusStop():
    """Test updating a bus stop"""
    # First create a bus stop
    id = create_BusStops_helper()

    # Then update it
    response = client.put(
        f"/api/bus_stops/{id}",
        json={"routes_served": "28X"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["routes_served"] == "28X"


def test_delete_BusStop():
    """Test deleting a bus stop"""
    # First create a bus stop
    id = create_BusStops_helper()

    # Then delete it
    response = client.delete(f"/api/bus_stops/{id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/api/bus_stops/{id}")
    assert response.status_code == 404


def test_get_nonexistent_bus_stop():
    """Test getting a bus stop that doesn't exist"""
    response = client.get("/api/bus_stops/99999")
    assert response.status_code == 404


def test_filter_by_route():
    """Test filtering bus stops by route"""
    response = client.get("/api/bus_stops/?routes_served=71D")
    assert response.status_code == 200


def test_search_BusStops():
    """Test searching bus stops"""
    response = client.get("/api/bus_stops/?search=Fifth Ave")
    assert response.status_code == 200


if __name__ == "__main__":
    print("Run with: pytest test_bus_stops_example.py -v")
