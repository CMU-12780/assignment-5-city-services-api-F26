from sqlalchemy.orm import Session
from sqlalchemy import or_             # necessary because search query in line 36
from typing import Optional
from .models import PublicPark
from .schemas import PublicParkCreate, PublicParkUpdate

def get_parks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    restroom: Optional[bool] = None,
    playground: Optional[bool] = None,
    sports_field: Optional[bool] = None,
    leash_free: Optional[bool] = None,
    search: Optional[str] = None,
    ) -> tuple[list[PublicPark], int]:   # return : tuple of (list of parks, total count)

    query = db.query(PublicPark)

    # filtered search
    if restroom is not None:
        query = query.filter(PublicPark.has_restroom == restroom)

    if playground is not None:
        query = query.filter(PublicPark.has_playground == playground)

    if leash_free is not None:
        query = query.filter(PublicPark.has_leash_free_zone == leash_free)

    if sports_field is not None:
        query = query.filter(PublicPark.has_sports_field == sports_field)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                PublicPark.park_name.ilike(search_term),
                PublicPark.address.ilike(search_term)
            )
        )

    # Get total count before pagination
    total = query.count()

    # Apply pagination and get results
    parks = query.offset(skip).limit(limit).all()

    return parks, total


def get_park(db: Session, park_id: int) -> Optional[PublicPark]:            # -> Optional[PublicPark]   promises to return park or none
    """Fetch specific park by ID"""
    return db.query(PublicPark).filter(PublicPark.id == park_id).first()


def create_park(db: Session, park_data: PublicParkCreate) -> PublicPark:    # -> PublicPark   promises to return park
    """Create new park"""
    park = PublicPark(**park_data.model_dump())
    db.add(park)
    db.commit()
    db.refresh(park)
    return park


def update_park(db: Session, park_id: int, park_data: PublicParkUpdate) -> Optional[PublicPark]:
    """Update park info"""
    park = get_park(db, park_id)
    if not park:
        return None

    # Update only provided fields
    update_data = park_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(park, field, value)

    db.commit()
    db.refresh(park)
    return park


def delete_park(db: Session, park_id: int) -> bool:   # Return True if deleted and False if not
    """Delete park"""
    park = get_park(db, park_id)
    if not park:
        return False

    db.delete(park)
    db.commit()
    return True
