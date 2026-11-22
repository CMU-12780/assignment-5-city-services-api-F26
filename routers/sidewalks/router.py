"""
Sidewalk Router
FastAPI endpoints for sidewalk management
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from .models import Sidewalk, SidewalkCondition
from .schemas import SidewalkCreate, SidewalkUpdate, SidewalkResponse, SidewalkListResponse
from . import crud

router = APIRouter()


@router.get("/", response_model=SidewalkListResponse)
def list_sidewalks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    condition: Optional[SidewalkCondition] = Query(None, description="Filter by condition"),
    ada_compliant: Optional[bool] = Query(None, description="Filter by ADA compliance"),
    surface_material: Optional[str] = Query(None, description="Filter by surface material"),
    search: Optional[str] = Query(None, description="Search in street name or block number"),
    db: Session = Depends(get_db)
) -> SidewalkListResponse:
    """
    List all sidewalks with optional filtering
    - **skip**: Pagination offset
    - **limit**: Maximum number of results
    - **condition**: Filter by condition rating (excellent, good, fair, poor)
    - **ada_compliant**: Filter by ADA compliance (true or false)
    - **surface_material**: Filter by surface material, e.g. concrete (case-insensitive)
    - **search**: Search term for street name or block number (case-insensitive)
    """
    sidewalks, total = crud.get_sidewalks(
        db=db,
        skip=skip,
        limit=limit,
        condition=condition,
        ada_compliant=ada_compliant,
        surface_material=surface_material,
        search=search
    )
    return SidewalkListResponse(total=total, sidewalks=sidewalks)


@router.post("/", response_model=SidewalkResponse, status_code=status.HTTP_201_CREATED)
def create_sidewalk(
    sidewalk: SidewalkCreate,
    db: Session = Depends(get_db)
) -> Sidewalk:
    """
    Create a new sidewalk
    Provide all required sidewalk information including:
    - Street name and block number
    - Physical dimensions (length, width)
    - Surface material
    - Current condition and ADA compliance
    """
    return crud.create_sidewalk(db=db, sidewalk_data=sidewalk)


@router.get("/{sidewalk_id}", response_model=SidewalkResponse)
def get_sidewalk(
    sidewalk_id: int,
    db: Session = Depends(get_db)
) -> Sidewalk:
    """
    Get a specific sidewalk by ID
    Returns detailed information about a single sidewalk section.
    """
    sidewalk = crud.get_sidewalk(db=db, sidewalk_id=sidewalk_id)
    if not sidewalk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sidewalk with id {sidewalk_id} not found"
        )
    return sidewalk


@router.put("/{sidewalk_id}", response_model=SidewalkResponse)
def update_sidewalk(
    sidewalk_id: int,
    sidewalk: SidewalkUpdate,
    db: Session = Depends(get_db)
) -> Sidewalk:
    """
    Update an existing sidewalk
    All fields are optional - only provided fields will be updated.
    Use this to update condition ratings, repair dates, or any other sidewalk information.
    """
    updated_sidewalk = crud.update_sidewalk(db=db, sidewalk_id=sidewalk_id, sidewalk_data=sidewalk)
    if not updated_sidewalk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sidewalk with id {sidewalk_id} not found"
        )
    return updated_sidewalk


@router.delete("/{sidewalk_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sidewalk(
    sidewalk_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a sidewalk
    Permanently removes a sidewalk from the system.
    Returns 204 No Content on success.
    """
    deleted = crud.delete_sidewalk(db=db, sidewalk_id=sidewalk_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sidewalk with id {sidewalk_id} not found"
        )
    return None
