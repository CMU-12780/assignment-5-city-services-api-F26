from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from .schemas import PublicParkCreate, PublicParkUpdate, PublicParkResponse, PublicParkListResponse
from . import crud

router = APIRouter()

@router.get("/", response_model=PublicParkListResponse)
def list_parks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),              # skip & limit functions as a manual page system
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),

    restroom: Optional[bool] = Query(None, description="Filter parks by restroom availability"),
    playground: Optional[bool] = Query(None, description="Filter parks by playground availability"),
    leash_free: Optional[bool] = Query(None, description="Filter parks by leash free zone availability"),
    sports_field: Optional[bool] = Query(None, description="Filter parks by sports field availability"),
    search: Optional[str] = Query(None, description="Search by park name or address"),

    db: Session = Depends(get_db)
) -> PublicParkListResponse:
    """List parks that fits filter"""
    parks, total = crud.get_parks(
        db=db,
        skip=skip,
        limit=limit,
        restroom=restroom,
        playground=playground,
        leash_free=leash_free,
        sports_field=sports_field,
        search=search
    )
    return PublicParkListResponse(total=total, parks=parks)


@router.post("/", response_model=PublicParkResponse, status_code=status.HTTP_201_CREATED)
def create_park(
    park: PublicParkCreate,
    db: Session = Depends(get_db)
) -> PublicParkResponse:
    """Create new park"""
    return crud.create_park(db=db, park_data=park)


@router.get("/{park_id}", response_model=PublicParkResponse)
def get_park(
    park_id: int, 
    db: Session = Depends(get_db)
) -> PublicParkResponse:
    """Fetch specific park by ID"""
    park = crud.get_park(db=db, park_id=park_id)
    if not park:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Park with id {park_id} not found"
        )
    return park


@router.put("/{park_id}", response_model=PublicParkResponse)
def update_park(
    park_id: int,
    park: PublicParkUpdate,
    db: Session = Depends(get_db)
) -> PublicParkResponse:
    """Update park info"""
    updated_park = crud.update_park(db=db, park_id=park_id, park_data=park)
    if not updated_park:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Park with id {park_id} not found"
        )
    return updated_park


@router.delete("/{park_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_park(
    park_id: int, 
    db: Session = Depends(get_db)
):
    """Delete park"""
    deleted = crud.delete_park(db=db, park_id=park_id)
    if not deleted:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Park with id {park_id} not found"
                )
    return None