from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from .models import PublicParkMaintenance

class PublicParkBase(BaseModel):
    # Fields for create/update
    """Base park schema with common fields"""
    park_name: str = Field(..., min_length=1, max_length=200, description="Name of Public Park")
    address: str = Field(..., min_length=1, max_length=500, description="Park Address")
    area_hectares: float = Field(..., gt=0, description="Park size in hectares")

    has_playground: bool = Field(False, description="Does this park have playground(s)?")
    has_restroom: bool = Field(False, description="Does this park have restroom(s)?")
    has_sports_field: bool = Field(False, description="Does this park have sports field(s)?")
    has_leash_free_zone: bool = Field(False, description="Does this park have leash free zone(s)?")
    has_blue_space: bool = Field(False, description="Does this park have blue space (ponds, creeks, lakes, etc.)?")

    num_bench: int = Field(0, ge=0, description="How many benches does this park have?")
    num_trash_bin: int = Field(0, ge=0, description="How many trash bins does this park have?")
    num_drinking_fountain: int = Field(0, ge=0, description="How many drinking fountains does this park have?")
    daily_visitors_avg: float = Field(0.0, ge=0, description="How many people visit this park on average per day?")

    maintenance_freq: PublicParkMaintenance = Field(..., description="How often is this park maintained?")


class PublicParkCreate(PublicParkBase):
    pass


class PublicParkUpdate(BaseModel):
    """Schema for updating a park - all fields optional"""
    park_name: Optional[str] = Field(None, min_length=1, max_length=200) 
    address: Optional[str] = Field(None, min_length=1, max_length=500) 
    area_hectares: Optional[float] = Field(None, gt=0)

    has_playground: Optional[bool] = Field(None)
    has_restroom: Optional[bool] = Field(None)
    has_sports_field: Optional[bool] = Field(None)
    has_leash_free_zone: Optional[bool] = Field(None)
    has_blue_space: Optional[bool] = Field(None)

    num_bench: Optional[int] = Field(None, ge=0)
    num_trash_bin: Optional[int] = Field(None, ge=0)
    num_drinking_fountain: Optional[int] = Field(None, ge=0)
    daily_visitors_avg: Optional[float] = Field(None, ge=0.0)

    maintenance_freq: Optional[PublicParkMaintenance] = Field(None)


class PublicParkResponse(PublicParkBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PublicParkListResponse(BaseModel):
    total: int
    parks: list[PublicParkResponse]