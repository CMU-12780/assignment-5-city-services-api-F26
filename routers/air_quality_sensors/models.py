from sqlalchemy import Column, String, Float, Integer, Date, Enum as SQLEnum
from models.base import BaseModel
import enum
# model code for air quality sensors

class SensorStatus(str, enum.Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class AirQualitySensor(BaseModel):
    """Air quality sensor"""
    __tablename__ = "air_quality_sensors"

    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    pm25 = Column(Float, nullable=True)
    aqi = Column(Integer, nullable=True)
    status = Column(SQLEnum(SensorStatus), nullable=False, default=SensorStatus.ACTIVE)
    install_date = Column(Date, nullable=True)