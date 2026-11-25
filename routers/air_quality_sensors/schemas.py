from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional
from .models import SensorStatus
# schemas code for air quality sensors

class AirQualitySensorBase(BaseModel):
    name: str
    location: str
    latitude: float
    longitude: float
    pm25: Optional[float] = None
    aqi: Optional[int] = None
    status: SensorStatus
    install_date: Optional[date] = None


class AirQualitySensorCreate(AirQualitySensorBase):
    pass


class AirQualitySensorUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    pm25: Optional[float] = None
    aqi: Optional[int] = None
    status: Optional[SensorStatus] = None
    install_date: Optional[date] = None


class AirQualitySensorResponse(AirQualitySensorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AirQualitySensorListResponse(BaseModel):
    total: int
    sensors: list[AirQualitySensorResponse]