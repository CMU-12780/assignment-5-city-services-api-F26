"""Database operations for street lights."""
from sqlalchemy.orm import Session
from .models import LightType, StreetLight
from .schemas import StreetLightCreate, StreetLightUpdate


def get_streetlights(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    light_type: LightType | None = None,
    is_operational: bool | None = None,
    search: str | None = None,
) -> tuple[list[StreetLight], int]:
    """List street lights with filters, location search and pagination."""
    query = db.query(StreetLight)
    if light_type is not None:
        query = query.filter(StreetLight.light_type == light_type)
    if is_operational is not None:
        query = query.filter(StreetLight.is_operational == is_operational)
    if search:
        query = query.filter(StreetLight.location.ilike(f"%{search}%"))

    total = query.count()
    streetlights = query.order_by(StreetLight.id).offset(skip).limit(limit).all()
    return streetlights, total


def get_streetlight(db: Session, streetlight_id: int) -> StreetLight | None:
    """Find a street light by ID."""
    return db.query(StreetLight).filter(StreetLight.id == streetlight_id).first()


def create_streetlight(db: Session, streetlight_data: StreetLightCreate) -> StreetLight:
    """Save a new street light."""
    streetlight = StreetLight(**streetlight_data.model_dump())
    db.add(streetlight)
    db.commit()
    db.refresh(streetlight)
    return streetlight


def update_streetlight(
    db: Session, streetlight_id: int, streetlight_data: StreetLightUpdate
) -> StreetLight | None:
    """Update only the supplied fields of an existing street light."""
    streetlight = get_streetlight(db, streetlight_id)
    if streetlight is None:
        return None
    for field, value in streetlight_data.model_dump(exclude_unset=True).items():
        setattr(streetlight, field, value)
    db.commit()
    db.refresh(streetlight)
    return streetlight


def delete_streetlight(db: Session, streetlight_id: int) -> bool:
    """Delete a street light, returning false if the ID does not exist."""
    streetlight = get_streetlight(db, streetlight_id)
    if streetlight is None:
        return False
    db.delete(streetlight)
    db.commit()
    return True
