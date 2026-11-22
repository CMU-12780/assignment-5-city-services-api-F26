"""
Road Router
FastAPI endpoints for road section management
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from .models import RoadSectionCondition, RoadSectionMaterial
from .schemas import RoadSectionCreate, RoadSectionUpdate, RoadSectionResponse, RoadSectionListResponse
from . import crud

router = APIRouter()


@router.get("/", response_model=RoadSectionListResponse)
def list_road_sections(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    condition: Optional[RoadSectionCondition] = Query(None, description="Filter by condition"),
    surface: Optional[RoadSectionMaterial] = Query(None, description="Filter by surface"),
    search: Optional[str] = Query(None, description="Search by street name"),
    db: Session = Depends(get_db)
):
    """
    List all road sections with optional filtering
    - **skip**: Pagination offset
    - **limit**: Maximum number of results
    - **condition**: Filter by condition rating (excellent, good, fair, poor, failed)
    - **surface**: Filter by surface type (asphalt, concrete, gravel, brick)
    - **search**: Search term for street name (case-insensitive)
    """
    road_sections, total = crud.get_road_sections(
        db=db,
        skip=skip,
        limit=limit,
        condition=condition,
        surface = surface,
        search=search
    )
    return RoadSectionListResponse(total=total, road_sections = road_sections)


@router.post("/", response_model=RoadSectionResponse, status_code=status.HTTP_201_CREATED)
def create_road_section(
    road_section: RoadSectionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new road section
    Provide all required road section information including:
    - Street name 
    - Section Start Point
    - Section End Point
    - Length in Kilometers
    - Number of Lanes
    - Surface type
    - Condition Rating
    - Last Resurfacing Date
    - Average Daily Traffic
    """
    return crud.create_road_section(db=db, road_section_data=road_section)


@router.get("/{road_section_id}", response_model=RoadSectionResponse)
def get_road_section(
    road_section_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific road section by ID
    Returns detailed information about a single road section.
    """
    road_section= crud.get_road_section(db=db, road_section_id=road_section_id)
    if not road_section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Road Section with id {road_section_id} not found"
        )
    return road_section


@router.put("/{road_section_id}", response_model=RoadSectionResponse)
def update_road_section(
    road_section_id: int,
    road_section: RoadSectionUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing road section
    All fields are optional - only provided fields will be updated.
    Use this to update inspection dates, condition ratings, or any other road section information.
    """
    updated_road_section = crud.update_road_section(db=db, road_section_id=road_section_id, road_section_data=road_section)
    if not updated_road_section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Road Section with id {road_section_id} not found"
        )
    return updated_road_section


@router.delete("/{road_section_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_road_section(
    road_section_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a road section
    Permanently removes a road section from the system.
    Returns 204 No Content on success.
    """
    deleted = crud.delete_road_section(db=db, road_section_id=road_section_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Road Section with id {road_section_id} not found"
        )
    return None
