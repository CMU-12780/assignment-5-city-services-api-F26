"""
Test file for Sidewalks router

To run tests:
1. Install pytest: pip install pytest httpx2
2. Run: pytest test_sidewalks.py -v
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_sidewalk_helper(full_result=False, **overrides):
    """Helper to create a new sidewalk; keyword arguments override default fields"""
    payload = {
        "street_name": "Test Street",
        "block_number": "100",
        "length_meters": 50.0,
        "width_meters": 1.5,
        "surface_material": "concrete",
        "condition": "good",
        "ada_compliant": True,
        "last_repair_date": "2024-06-15"
    }
    payload.update(overrides)
    response = client.post("/api/sidewalks/", json=payload)
    if full_result:
        return response
    else:
        data = response.json()
        return data["id"]


def test_create_sidewalk():
    """Test creating a new sidewalk"""
    response = create_sidewalk_helper(full_result=True)
    assert response.status_code == 201
    data = response.json()
    assert data["street_name"] == "Test Street"
    assert data["block_number"] == "100"
    assert data["ada_compliant"] is True
    assert "id" in data


def test_list_sidewalks():
    """Test listing all sidewalks"""
    response = client.get("/api/sidewalks/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "sidewalks" in data
    assert isinstance(data["sidewalks"], list)


def test_get_sidewalk():
    """Test getting a specific sidewalk"""
    # First create a sidewalk
    sidewalk_id = create_sidewalk_helper()

    # Then retrieve it
    response = client.get(f"/api/sidewalks/{sidewalk_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sidewalk_id


def test_update_sidewalk():
    """Test updating a sidewalk"""
    # First create a sidewalk
    sidewalk_id = create_sidewalk_helper()

    # Then update it
    response = client.put(
        f"/api/sidewalks/{sidewalk_id}",
        json={"condition": "fair"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["condition"] == "fair"
    # Fields not sent in the update should stay unchanged
    assert data["street_name"] == "Test Street"


def test_delete_sidewalk():
    """Test deleting a sidewalk"""
    # First create a sidewalk
    sidewalk_id = create_sidewalk_helper()

    # Then delete it
    response = client.delete(f"/api/sidewalks/{sidewalk_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/api/sidewalks/{sidewalk_id}")
    assert response.status_code == 404


def test_get_nonexistent_sidewalk():
    """Test getting a sidewalk that doesn't exist"""
    response = client.get("/api/sidewalks/99999")
    assert response.status_code == 404


def test_update_nonexistent_sidewalk():
    """Test updating a sidewalk that doesn't exist"""
    response = client.put("/api/sidewalks/99999", json={"condition": "poor"})
    assert response.status_code == 404


def test_delete_nonexistent_sidewalk():
    """Test deleting a sidewalk that doesn't exist"""
    response = client.delete("/api/sidewalks/99999")
    assert response.status_code == 404


def test_filter_by_condition():
    """Test filtering sidewalks by condition"""
    create_sidewalk_helper()
    response = client.get("/api/sidewalks/?condition=good")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all(s["condition"] == "good" for s in data["sidewalks"])


def test_filter_by_ada_compliant():
    """Test filtering sidewalks by ADA compliance"""
    create_sidewalk_helper()
    response = client.get("/api/sidewalks/?ada_compliant=true")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all(s["ada_compliant"] is True for s in data["sidewalks"])

    # Filtering for False must not return compliant sidewalks
    response = client.get("/api/sidewalks/?ada_compliant=false")
    assert response.status_code == 200
    data = response.json()
    assert all(s["ada_compliant"] is False for s in data["sidewalks"])


def test_filter_by_surface_material():
    """Test filtering sidewalks by surface material (case-insensitive)"""
    create_sidewalk_helper(surface_material="brick")
    response = client.get("/api/sidewalks/?surface_material=Brick")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all(s["surface_material"].lower() == "brick" for s in data["sidewalks"])


def test_search_sidewalks():
    """Test searching sidewalks by street name"""
    create_sidewalk_helper()
    response = client.get("/api/sidewalks/?search=test")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all(
        "test" in s["street_name"].lower() or "test" in s["block_number"].lower()
        for s in data["sidewalks"]
    )


def test_search_sidewalks_by_block_number():
    """Test that search also matches the block number"""
    create_sidewalk_helper(street_name="Forbes Avenue", block_number="BLK-5000")
    response = client.get("/api/sidewalks/?search=blk-5000")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all("blk-5000" in s["block_number"].lower() for s in data["sidewalks"])


def test_create_sidewalk_invalid_data():
    """Test that invalid data is rejected"""
    response = create_sidewalk_helper(full_result=True, length_meters=-5.0)
    assert response.status_code == 422


if __name__ == "__main__":
    print("Run with: pytest test_sidewalks.py -v")
