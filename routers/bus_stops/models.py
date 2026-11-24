from sqlalchemy import Column, String, Float, Date, Integer, Boolean
from models.base import BaseModel

class BusStops(BaseModel):
    __tablename__ = "bus_stops"
    
    # Add your fields here
    bus_stop_id = Column(String, nullable=False, index=True)
    location = Column(String, nullable=False)
    routes_served = Column(String, nullable=False)
    has_shelter = Column(Boolean, default=False)
    has_bench = Column(Boolean, default=False)
    has_lighting = Column(Boolean, default=False)
    daily_boardings_avg = Column(Integer, nullable=True)
    last_maintenance = Column(Date, nullable=True)

    def __repr__(self):
        return f"<BusStops(bus_stop_id='{self.bus_stop_id}', routes='{self.routes_served}', location='{self.location}')>"
    