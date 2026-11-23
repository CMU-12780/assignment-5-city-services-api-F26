from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional
from .schemas import BusStopCreate, BusStopUpdate, BusStopResponse, BusStopListResponse
from . import crud 

router = APIRouter()

@router.get("/", response_model=BusStopListResponse)
def list_BusStops(
     skip: int = Query(0, ge=0, description="Number of records to skip"),
     limit: int = Query(100, ge=0, le=500, description="Maximum records to return"),
     stop_id_num: Optional[str] = Query(None, description="Search in name or location"),
     routes: Optional[str] = Query(None, description="Search in route numbers"),
     search: Optional[str] = Query(None, description="Search in name of location"),
     db: Session = Depends(get_db)):

    bus_stops , total = crud.get_BusStops(
        db=db,
        skip=skip,
        limit=limit,
        stop_id_num=stop_id_num,
        routes=routes,
        search=search
    )
    return BusStopListResponse(total=total, bus_stops=bus_stops)

@router.post("/", response_model=BusStopResponse, status_code=status.HTTP_201_CREATED)
def create_BusStop(
    bus_stop: BusStopCreate,
    db: Session = Depends(get_db)
):
    return crud.create_BusStop(db=db, bus_stop_data = bus_stop)

@router.get("/{bus_stop_id}", response_model=BusStopResponse)
def get_BusStops(bus_stop_id: int, db: Session = Depends(get_db)):
    bus_stop = crud.get_BusStop(db=db, bus_stop_id=bus_stop_id)
    if not bus_stop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Bus Stop with id {bus_stop_id} not found'
        )
    return bus_stop

@router.put("/{bus_stop_id}", response_model=BusStopResponse)
def update_BusStop(bus_stop_id: int, bus_stop: BusStopUpdate, db: Session = Depends(get_db)):
    updated_bus_stop = crud.update_BusStop(db=db, bus_stop_id=bus_stop_id,bus_stop_data=bus_stop)
    if not updated_bus_stop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bus Stop with id {bus_stop_id} not found"
        )
    return updated_bus_stop

@router.delete("/{bus_stop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(bus_stop_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_BusStop(db=db, bus_stop_id=bus_stop_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bus Stop with id {bus_stop_id} not found"
        )
    return None