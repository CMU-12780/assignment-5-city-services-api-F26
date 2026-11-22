"""
Road Sections database model
"""
from sqlalchemy import Column, Integer, String, Float, Date, Enum as SQLEnum
from models.base import BaseModel
import enum


class RoadSectionCondition(str, enum.Enum):
    """Road section condition ratings"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    FAILED = "failed"

class RoadSectionMaterial(str, enum.Enum):
    """Road section material type"""
    ASPHALT = "asphalt"
    CONCRETE = "concrete"
    GRAVEL = "gravel"
    BRICK = "brick"

class RoadSection(BaseModel):
    """
    Road section infrastructure model
    Tracks Road section inspections, conditions, and maintenance
    """
    __tablename__ = "road_sections"

    # Basic Information
    street_name = Column(String, nullable=False, index=True)
    start_address = Column(String, nullable=False)
    end_address = Column(String, nullable=False)
    length_km = Column(Float, nullable=False)
    lanes_count = Column(Integer, nullable=False)
    surface_type = Column(SQLEnum(RoadSectionMaterial), nullable=False, default=RoadSectionMaterial.CONCRETE)
    condition_rating = Column(SQLEnum(RoadSectionCondition), nullable=False, default=RoadSectionCondition.GOOD)
    last_resurfaced = Column(Date, nullable=True)
    average_daily_traffic = Column(Integer, nullable= True)

    # Notes
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<RoadSection(id={self.id}, name='{self.street_name}', condition='{self.condition_rating}')>"
