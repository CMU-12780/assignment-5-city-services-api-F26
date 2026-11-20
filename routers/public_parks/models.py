from sqlalchemy import Column, String, Float, Boolean, Integer, Enum as SQLEnum
from models.base import BaseModel
import enum


class PublicParkMaintenance(str, enum.Enum) :
    # give dropdown options to select maintenance frequency
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    BIMONTHLY = "bimonthly"
    QUARTERLY = "quarterly"
    BIANNUALLY = "biannually"
    ANNUALLY = "annually"

class PublicPark(BaseModel):
    __tablename__ = "public_parks"
    
    # Basic Info
    park_name = Column(String, nullable=False, index=True)     # Indexed
    address = Column(String, nullable=False)
    area_hectares = Column(Float, nullable=False)

    # Additional Info
    has_playground = Column(Boolean, nullable=False, default=False)
    has_sports_field = Column(Boolean, nullable=False, default=False)
    has_restroom = Column(Boolean, nullable=False, default=False)
    has_leash_free_zone = Column(Boolean, nullable=False, default=False)
    has_blue_space = Column(Boolean, nullable=False, default=False)

    num_bench = Column(Integer, nullable=False, default=0)
    num_trash_bin = Column(Integer, nullable=False, default=0)
    num_drinking_fountain = Column(Integer, nullable=False, default=0)
    daily_visitors_avg = Column(Float, nullable=False, default=0)             # changed it to float since average may not be an integer

    maintenance_freq = Column(SQLEnum(PublicParkMaintenance), nullable=False)  # choose from dropdown options

    def __repr__(self):
        return f"<PublicPark(id={self.id}, name='{self.park_name}', area_hectares='{self.area_hectares}')>"
