"""Database model for city street lights."""
from enum import Enum
from sqlalchemy import Boolean, Column, Date, Float, Integer, String
from sqlalchemy import Enum as SQLEnum
from models.base import BaseModel


class LightType(str, Enum):
    """Supported street light types."""
    LED = "LED"
    SODIUM = "Sodium"
    HALOGEN = "Halogen"


class StreetLight(BaseModel):
    """A street light with location, power and maintenance information."""
    __tablename__ = "streetlights"

    location = Column(String, nullable=False)
    pole_id = Column(String, nullable=False, unique=True, index=True)
    light_type = Column(SQLEnum(LightType), nullable=False)
    wattage = Column(Integer, nullable=False)
    installation_date = Column(Date, nullable=True)
    last_maintenance = Column(Date, nullable=True)
    is_operational = Column(Boolean, nullable=False, default=True)
    energy_consumption_kwh = Column(Float, nullable=True)
