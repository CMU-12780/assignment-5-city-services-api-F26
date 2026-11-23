from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional

class BusStopsBase(BaseModel):
    """Base bus stop schema with common fields"""
    bus_stop_id: str = Field(...,min_length=1, max_length=50,
                         description="Unique Stop Identifier")
    location: str = Field(...,min_length=1,max_length=200,
                          description="Street Address or Intersection")
    routes_served: str = Field(..., min_length=1,max_length=50, 
                               description="Route Numbers (e.g. 1, 5, 22)")
    has_shelter: bool = Field(default=False, description="Shelter Present")
    has_bench: bool = Field(default=False, description="Bench Available")
    has_lighting: bool = Field(default=False, description="Lighting Installed")
    daily_boardings_avg: int = Field(...,description="Average Daily Boardings")
    last_maintenance: Optional[str] = Field(None, description="Last Maintenance Date")
    
class BusStopCreate(BusStopsBase):
    """Schema for creating a new bus stop"""
    pass

class BusStopUpdate(BaseModel):
    """Schema for updating a bus stop - all fields optional"""
    bus_stop_id: Optional[str] = Field(None,min_length=1, max_length=50)
    location: Optional[str] = Field(None,min_length=1,max_length=200)
    routes_served: Optional[str] = Field(None, min_length=1,max_length=50)
    has_shelter: Optional[bool] = None
    has_bench: Optional[bool] = None
    has_lighting: Optional[bool] = None
    daily_boardings_avg: Optional[int] = Field(None)
    last_maintenance: Optional[str] = None

class BusStopResponse(BusStopsBase):
    """Schema for bus stop response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class BusStopListResponse(BaseModel):
    """Schema for list of bus stops"""
    total: int
    bus_stops: list[BusStopResponse]