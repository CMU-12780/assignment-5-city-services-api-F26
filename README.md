# City Infrastructure Monitoring API

A FastAPI project for monitoring municipal infrastructure. Please contribute an independent router module for a different infrastructure type (17 types total: street lights, traffic signals, water quality, potholes, trees, parking meters, fire hydrants, building permits, noise complaints, sidewalks, public parks, bus stops, bike lanes, air quality sensors, storm drains, crosswalks, and road sections). Bridges is provided as a complete worked example.

## Project Structure

```
assignment-5-city-services-api-F26/
├── main.py                      # Main FastAPI application
├── database.py                  # Database configuration
├── requirements.txt             # Python dependencies
├── models/
│   ├── __init__.py
│   └── base.py                 # Base SQLAlchemy model
├── schemas/
│   ├── __init__.py
│   └── base.py                 # Base Pydantic schemas
└── routers/
    ├── __init__.py
    └── bridges/                # Example router (complete)
        ├── __init__.py
        ├── router.py           # FastAPI endpoints
        ├── models.py           # SQLAlchemy model
        ├── schemas.py          # Pydantic schemas
        └── crud.py             # Database operations
```

## Setup Instructions

### 1. Install Dependencies

Requires Python 3.13 or 3.14.

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

### 3. View API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing the Bridges Example

### Create a Bridge (POST)

```bash
curl -X POST "http://localhost:8000/api/bridges/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Golden Gate Bridge",
    "location": "San Francisco, CA",
    "length_meters": 2737,
    "width_meters": 27,
    "max_load_rating_tons": 100,
    "condition": "good",
    "year_built": "1937",
    "material": "steel"
  }'
```

### List All Bridges (GET)

```bash
curl "http://localhost:8000/api/bridges/"
```

### Get Specific Bridge (GET)

```bash
curl "http://localhost:8000/api/bridges/1"
```

### Update Bridge (PUT)

```bash
curl -X PUT "http://localhost:8000/api/bridges/1" \
  -H "Content-Type: application/json" \
  -d '{
    "condition": "fair",
    "last_inspection_date": "2024-11-01"
  }'
```

### Delete Bridge (DELETE)

```bash
curl -X DELETE "http://localhost:8000/api/bridges/1"
```

## Street Lights Router (Issue #1)

The Street Lights module is in `routers/streetlights/` and is registered at
`/api/streetlights`. It follows the Bridges example and stores eight fields:
`location`, `pole_id`, `light_type`, `wattage`, `installation_date`,
`last_maintenance`, `is_operational`, and `energy_consumption_kwh`.
IDs and creation/update timestamps are inherited from the shared base model.

### Endpoints

| Method | URL | Result |
| --- | --- | --- |
| GET | `/api/streetlights/` | List street lights (200) |
| POST | `/api/streetlights/` | Create a street light (201) |
| GET | `/api/streetlights/{id}` | Get a street light (200) |
| PUT | `/api/streetlights/{id}` | Update the supplied fields (200) |
| DELETE | `/api/streetlights/{id}` | Delete a street light (204, empty body) |

Missing IDs return 404. Pole IDs must be unique; duplicates return 409.
Invalid input returns 422. Location and pole ID cannot be blank, wattage must
be a positive integer, and monthly energy consumption cannot be negative.
Light types are `LED`, `Sodium`, and `Halogen`. Dates use `YYYY-MM-DD`.
Optional dates and energy consumption may be cleared with `null` in a PUT;
required fields may be omitted in a PUT but cannot be set to `null`.

### Try it

Start the application using the setup instructions above, then open
`http://localhost:8000/docs` and expand **Street Lights**. Example POST body:

```json
{
  "location": "Forbes Avenue, Pittsburgh",
  "pole_id": "PIT-001",
  "light_type": "LED",
  "wattage": 80,
  "installation_date": "2024-05-01",
  "last_maintenance": "2026-11-01",
  "is_operational": true,
  "energy_consumption_kwh": 28.8
}
```

The list endpoint accepts `light_type`, `is_operational`, and a case-insensitive
`search` on location. Filters can be combined. Use `skip` and `limit` for
pagination (default limit 100, maximum 500). The returned `total` is the number
of matching records before pagination.

```bash
curl "http://localhost:8000/api/streetlights/?light_type=LED&is_operational=false&search=Forbes"
python -m pytest test_streetlights.py test_bridges_example.py -v
```

Street Lights tests use a fresh in-memory SQLite database for each test.
They cover CRUD, filters, search, pagination, validation, duplicate pole IDs,
missing IDs, and OpenAPI registration. The original Bridges tests also pass.

## Student Assignment Instructions

### Your Task

Create a complete router module for your assigned infrastructure type following the Bridges example pattern.

### Step-by-Step Instructions

#### 1. Create Your Router Directory

```bash
mkdir -p routers/your_resource
cd routers/your_resource
touch __init__.py models.py schemas.py crud.py router.py
```

Replace `your_resource` with your assignment (e.g., `streetlights`, `traffic_signals`, etc.)

#### 2. Create Your Model (`models.py`)

Define your SQLAlchemy database model:

```python
from sqlalchemy import Column, String, Float, Date, Integer
from models.base import BaseModel

class YourResource(BaseModel):
    __tablename__ = "your_resources"
    
    # Add your fields here
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    # ... add 5-8 relevant fields
```

**Key Requirements:**
- Inherit from `BaseModel` (gives you `id`, `created_at`, `updated_at`)
- Include at least 5-8 meaningful fields
- Use appropriate data types (String, Float, Integer, Date, etc.)
- Consider using Enums for categorical data (like condition ratings)

#### 3. Create Your Schemas (`schemas.py`)

Define Pydantic models for validation:

```python
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class YourResourceBase(BaseModel):
    # Fields for create/update
    pass

class YourResourceCreate(YourResourceBase):
    pass

class YourResourceUpdate(BaseModel):
    # All fields optional
    pass

class YourResourceResponse(YourResourceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class YourResourceListResponse(BaseModel):
    total: int
    resources: list[YourResourceResponse]
```

#### 4. Create CRUD Operations (`crud.py`)

Implement database operations:

```python
from sqlalchemy.orm import Session
from typing import Optional
from .models import YourResource
from .schemas import YourResourceCreate, YourResourceUpdate

def get_resources(db: Session, skip: int = 0, limit: int = 100):
    # Implementation
    pass

def get_resource(db: Session, resource_id: int):
    # Implementation
    pass

def create_resource(db: Session, resource_data: YourResourceCreate):
    # Implementation
    pass

def update_resource(db: Session, resource_id: int, resource_data: YourResourceUpdate):
    # Implementation
    pass

def delete_resource(db: Session, resource_id: int):
    # Implementation
    pass
```

#### 5. Create Your Router (`router.py`)

Implement the 5 required endpoints:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

@router.get("/")
def list_resources(db: Session = Depends(get_db)):
    # GET all resources
    pass

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_resource(db: Session = Depends(get_db)):
    # POST new resource
    pass

@router.get("/{resource_id}")
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    # GET single resource
    pass

@router.put("/{resource_id}")
def update_resource(resource_id: int, db: Session = Depends(get_db)):
    # PUT update resource
    pass

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    # DELETE resource
    pass
```

#### 6. Update `__init__.py`

```python
"""Your Resource router package"""
from .router import router

__all__ = ["router"]
```

#### 7. Register Your Router in `main.py`

Add these lines to `main.py`:

```python
from routers.your_resource import router as your_resource_router

app.include_router(
    your_resource_router, 
    prefix="/api/your-resource", 
    tags=["Your Resource"]
)
```

### Requirements Checklist

- [ ] Model with 5-8 relevant fields
- [ ] All Pydantic schemas (Base, Create, Update, Response, ListResponse)
- [ ] All 5 CRUD functions implemented
- [ ] All 5 router endpoints with proper:
  - [ ] HTTP methods (GET, POST, PUT, DELETE)
  - [ ] Status codes
  - [ ] Response models
  - [ ] Error handling (404s)
  - [ ] Docstrings
- [ ] Router registered in `main.py`
- [ ] Code tested with curl or browser
- [ ] Follows the Bridges example pattern
- [ ] Test Resource file that follows the `test_bridges_example.py` pattern
- [ ] 100% pass rate for unit test file

### Testing Your Router

1. Start the server: `python main.py`
2. Visit: http://localhost:8000/docs
3. Test all 5 endpoints in the Swagger UI
4. Verify:
   - Can create records
   - Can list all records
   - Can get single record
   - Can update records
   - Can delete records
   - Proper error messages for invalid IDs

5. Create your own test_your_resource.py and ensure all tests pass

## Common Issues & Solutions

### Issue: "Table already exists" error
**Solution**: Delete `city_infrastructure.db` and restart

### Issue: Import errors
**Solution**: Make sure all `__init__.py` files exist

### Issue: 422 Validation Error
**Solution**: Check your Pydantic schemas match your model

### Issue: Router not showing in /docs
**Solution**: Verify router is registered in `main.py`

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org
- **Pydantic Docs**: https://docs.pydantic.dev
