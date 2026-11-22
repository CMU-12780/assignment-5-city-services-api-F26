"""
Sidewalk database model
"""
from sqlalchemy import Column, String, Float, Date, Boolean, Enum as SQLEnum
from models.base import BaseModel
import enum


class SidewalkCondition(str, enum.Enum):
    """Sidewalk condition ratings"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class Sidewalk(BaseModel):
    """
    Sidewalk infrastructure model
    Tracks sidewalk sections, their condition, and ADA compliance
    """
    __tablename__ = "sidewalks"

    # Location
    street_name = Column(String, nullable=False, index=True)
    block_number = Column(String, nullable=False)

    # Physical dimensions
    length_meters = Column(Float, nullable=False)
    width_meters = Column(Float, nullable=False)
    surface_material = Column(String, nullable=False)  # e.g., "concrete", "asphalt"

    # Condition and accessibility
    condition = Column(SQLEnum(SidewalkCondition), nullable=False)
    ada_compliant = Column(Boolean, nullable=False)

    # Maintenance
    last_repair_date = Column(Date, nullable=True)

    def __repr__(self):
        return f"<Sidewalk(id={self.id}, street_name='{self.street_name}', condition='{self.condition}')>"
