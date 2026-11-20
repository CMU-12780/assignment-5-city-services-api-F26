"""Street light request validation and response schemas."""
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from .models import LightType


class StreetLightBase(BaseModel):
    """Common street light fields."""
    model_config = ConfigDict(str_strip_whitespace=True)

    location: str = Field(..., min_length=1, max_length=300)
    pole_id: str = Field(..., min_length=1, max_length=100)
    light_type: LightType
    wattage: int = Field(..., gt=0)
    installation_date: date | None = None
    last_maintenance: date | None = None
    is_operational: bool = True
    energy_consumption_kwh: float | None = Field(None, ge=0, allow_inf_nan=False)


class StreetLightCreate(StreetLightBase):
    """Fields used to create a street light."""
    pass


class StreetLightUpdate(BaseModel):
    """Optional fields for a partial update; dates and energy may be cleared."""
    model_config = ConfigDict(str_strip_whitespace=True)

    location: str | None = Field(None, min_length=1, max_length=300)
    pole_id: str | None = Field(None, min_length=1, max_length=100)
    light_type: LightType | None = None
    wattage: int | None = Field(None, gt=0)
    installation_date: date | None = None
    last_maintenance: date | None = None
    is_operational: bool | None = None
    energy_consumption_kwh: float | None = Field(None, ge=0, allow_inf_nan=False)

    @model_validator(mode="after")
    def reject_null_required_fields(self) -> "StreetLightUpdate":
        """Allow fields to be omitted without allowing required columns to become null."""
        for field in ("location", "pole_id", "light_type", "wattage", "is_operational"):
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class StreetLightResponse(StreetLightBase):
    """A saved street light, including its ID and timestamps."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class StreetLightListResponse(BaseModel):
    """Filtered total and the current page of street lights."""
    total: int
    streetlights: list[StreetLightResponse]
