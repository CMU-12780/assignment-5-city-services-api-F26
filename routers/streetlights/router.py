"""FastAPI endpoints for street light management."""
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import get_db
from . import crud
from .models import LightType, StreetLight
from .schemas import (
    StreetLightCreate, StreetLightUpdate, StreetLightResponse, StreetLightListResponse,
)

router = APIRouter()


@router.get("/", response_model=StreetLightListResponse)
def list_streetlights(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    light_type: LightType | None = Query(None, description="LED, Sodium or Halogen"),
    is_operational: bool | None = Query(None, description="Filter by operational status"),
    search: str | None = Query(None, description="Search location, ignoring case"),
    db: Session = Depends(get_db),
) -> StreetLightListResponse:
    """List street lights with optional type, operational status and location filters."""
    streetlights, total = crud.get_streetlights(
        db, skip, limit, light_type, is_operational, search
    )
    return StreetLightListResponse(total=total, streetlights=streetlights)


@router.post("/", response_model=StreetLightResponse, status_code=status.HTTP_201_CREATED)
def create_streetlight(
    streetlight: StreetLightCreate, db: Session = Depends(get_db)
) -> StreetLight:
    """Create a street light with a unique pole ID; duplicates return 409."""
    try:
        return crud.create_streetlight(db, streetlight)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Pole ID already exists") from None


@router.get("/{streetlight_id}", response_model=StreetLightResponse)
def get_streetlight(streetlight_id: int, db: Session = Depends(get_db)) -> StreetLight:
    """Get one street light by ID, or return 404 if it does not exist."""
    streetlight = crud.get_streetlight(db, streetlight_id)
    if streetlight is None:
        raise HTTPException(status_code=404, detail=f"Street light with id {streetlight_id} not found")
    return streetlight


@router.put("/{streetlight_id}", response_model=StreetLightResponse)
def update_streetlight(
    streetlight_id: int, streetlight: StreetLightUpdate, db: Session = Depends(get_db)
) -> StreetLight:
    """Update supplied fields; missing IDs return 404 and duplicate pole IDs return 409."""
    try:
        updated = crud.update_streetlight(db, streetlight_id, streetlight)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Pole ID already exists") from None
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Street light with id {streetlight_id} not found")
    return updated


@router.delete("/{streetlight_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_streetlight(streetlight_id: int, db: Session = Depends(get_db)) -> Response:
    """Delete a street light with an empty 204 response, or return 404 for a missing ID."""
    if not crud.delete_streetlight(db, streetlight_id):
        raise HTTPException(status_code=404, detail=f"Street light with id {streetlight_id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
