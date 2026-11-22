"""
Example test file for Road Section router
Use this as a reference for testing your own routers

To run tests:
1. Install pytest: pip install pytest httpx2
2. Run: pytest test_road_sections_example.py -v
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_road_section_helper(full_result=False):
    """Helper to create a new road section"""
    response = client.post(
        "/api/road-sections/",
        json={
            "street_name": "523 West 160th Street",
            "start_address": "159th street",
            "end_address": "160th street",
            "length_km": 10,
            "lanes_count": 1,
            "surface_type": "asphalt",
            "condition_rating": "excellent",
            "last_resurfaced": "2026-11-22",
            "average_daily_traffic": 10,
            "notes": "It's still in excellent condition!"
        }
    )
    if full_result:
        return response
    else:
        data = response.json()
        return data["id"]

def test_create_road_section():
    """Test creating a new road section"""
    response = create_road_section_helper(full_result=True)
    assert response.status_code == 201
    data = response.json()
    assert data["street_name"] == "523 West 160th Street"
    assert "id" in data

def test_list_road_sections():
    """Test listing all road sections"""
    response = client.get("/api/road-sections/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "road_sections" in data
    assert isinstance(data["road_sections"], list)


def test_get_road_sections():
    """Test getting a specific road section"""
    # First create a road section
    road_section_id = create_road_section_helper()

    # Then retrieve it
    response = client.get(f"/api/road-sections/{road_section_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == road_section_id


def test_update_road_section():
    """Test updating a road section"""
    # First create a road section
    road_section_id = create_road_section_helper()

    # Then update it
    response = client.put(
        f"/api/road-sections/{road_section_id}",
        json={"condition_rating": "excellent"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["condition_rating"] == "excellent"


def test_delete_road_section():
    """Test deleting a road section"""
    # First create a road section
    road_section_id = create_road_section_helper()

    # Then delete it
    response = client.delete(f"/api/road-sections/{road_section_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/api/road-sections/{road_section_id}")
    assert response.status_code == 404


def test_get_nonexistent_road_section():
    """Test getting a road section that doesn't exist"""
    response = client.get("/api/road-sections/99999")
    assert response.status_code == 404


def test_filter_by_condition():
    """Test filtering road section by condition"""
    response = client.get("/api/road-sections/?condition=excellent")
    assert response.status_code == 200

def test_filter_by_surface_type():
    """Test filtering road section by surface type"""
    response = client.get("/api/road-sections/?surface=concrete")
    assert response.status_code == 200

def test_search_road_section():
    """Test searching road section"""
    response = client.get("/api/road-sections/?search=Test")
    assert response.status_code == 200


if __name__ == "__main__":
    print("Run with: pytest test_road_sections_example.py -v")
