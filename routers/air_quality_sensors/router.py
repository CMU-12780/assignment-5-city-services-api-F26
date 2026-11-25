from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from .schemas import (
    AirQualitySensorCreate,
    AirQualitySensorUpdate,
    AirQualitySensorResponse,
    AirQualitySensorListResponse,
)
from . import crud

router = APIRouter()# router for air quality sensors


@router.get("/", response_model=AirQualitySensorListResponse)
def list_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all air quality sensors"""
    sensors, total = crud.get_sensors(db, skip, limit)
    return {"total": total, "sensors": sensors}


@router.post("/", response_model=AirQualitySensorResponse, status_code=status.HTTP_201_CREATED)
def create_sensor(sensor: AirQualitySensorCreate, db: Session = Depends(get_db)):
    """Create a new sensor"""
    return crud.create_sensor(db, sensor)


@router.get("/{sensor_id}", response_model=AirQualitySensorResponse)
def get_sensor(sensor_id: int, db: Session = Depends(get_db)):
    """Get one sensor by id"""
    sensor = crud.get_sensor(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.put("/{sensor_id}", response_model=AirQualitySensorResponse)
def update_sensor(sensor_id: int, sensor: AirQualitySensorUpdate, db: Session = Depends(get_db)):
    """Update a sensor"""
    updated = crud.update_sensor(db, sensor_id, sensor)
    if not updated:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return updated


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(sensor_id: int, db: Session = Depends(get_db)):
    """Delete a sensor"""
    if not crud.delete_sensor(db, sensor_id):
        raise HTTPException(status_code=404, detail="Sensor not found")