"""
Road Section Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from .models import RoadSectionCondition, RoadSectionMaterial


class RoadSectionBase(BaseModel):
    """Base road section schema with common fields"""
    street_name: str = Field(..., min_length=1, max_length=200, description="Street name")
    start_address: str = Field(..., min_length=1, max_length=300, description="Start address")
    end_address: str = Field(..., min_length=1, max_length=300, description="End address")
    length_km: float = Field(..., gt=0, description="Road section length in kilometers")
    lanes_count: int = Field(..., gt=0, description="Lane count")
    surface_type: RoadSectionMaterial = Field(..., description="Surface type")
    condition_rating: RoadSectionCondition = Field(..., description="Current condition rating")
    last_resurfaced: Optional[date] = Field(None, description="Date of last resurface")
    average_daily_traffic: Optional[int] = Field(None, gt=0, description="Daily average traffic")
    notes: Optional[str] = Field(None, max_length=1000, description="Additional notes")

class RoadSectionCreate(RoadSectionBase):
    """Schema for creating a new road"""
    pass


class RoadSectionUpdate(BaseModel):
    """Schema for updating a road section - all fields optional"""
    street_name: Optional[str] = Field(None, min_length=1, max_length=200)
    start_address: Optional[str] = Field(None, min_length=1, max_length=300)
    end_address: Optional[str] = Field(None, min_length=1, max_length = 300)
    length_km: Optional[float] = Field(None, gt=0)
    lanes_count: Optional[int] = Field(None, gt=0)
    surface_type: Optional[RoadSectionMaterial] = None
    condition_rating: Optional[RoadSectionCondition] = None
    last_resurfaced: Optional[date] = None
    average_daily_traffic: Optional[int] = Field(None,gt=0)
    notes: Optional[str] = Field(None, max_length=1000)



class RoadSectionResponse(RoadSectionBase):
    """Schema for road section response"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RoadSectionListResponse(BaseModel):
    """Schema for list of road sections"""
    total: int
    road_sections: list[RoadSectionResponse]
