"""
Road Section CRUD operations
Database operations for road sections
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from .models import RoadSection, RoadSectionCondition,RoadSectionMaterial
from .schemas import RoadSectionCreate, RoadSectionUpdate


def get_road_sections(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    condition: Optional[RoadSectionCondition] = None,
    surface: Optional[RoadSectionMaterial] = None,
    search: Optional[str] = None
) -> tuple[list[RoadSection], int]:
    """
    This is used for searching for road sections via street name

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        condition: Filter by condition rating
        surface: Filter by surface_type
        search: Search term for street name or surface type

    Returns:
        Tuple of (list of road sections, total count)
    """
    query = db.query(RoadSection)

    # Apply filters
    if condition:
        query = query.filter(RoadSection.condition_rating == condition)

    if surface:
        query = query.filter(RoadSection.surface_type == surface) 


    if search:
        search_name = f"%{search}%"
        query = query.filter(RoadSection.street_name.ilike(search_name))

    
    

    # Get total count before pagination
    total = query.count()

    # Apply pagination and get results
    road_sections = query.offset(skip).limit(limit).all()

    return road_sections, total

#SINGULAR ONLY REMEMBER THAT
def get_road_section(db: Session, road_section_id: int) -> Optional[RoadSection]:
    """
    Get a specific road section by stret name or surface type

    Args:
        db: Database session
        road_section streetname: Road Section street name

    Returns:
        Road Section object or None if not found
    """
    return db.query(RoadSection).filter(RoadSection.id == road_section_id).first()


def create_road_section(db: Session, road_section_data: RoadSectionCreate) -> RoadSection:
    """
    Create a new road section

    Args:
        db: Database session
        road_section_data: Road Section creation data

    Returns:
        Created road section object
    """
    road_section = RoadSection(**road_section_data.model_dump())
    db.add(road_section)
    db.commit()
    db.refresh(road_section)
    return road_section


def update_road_section(
    db: Session,
    road_section_id: int,
    road_section_data: RoadSectionUpdate
) -> Optional[RoadSection]:
    """
    Update an existing road section

    Args:
        db: Database session
        road_section_id: Road Section ID
        road_section_data: Road Section update data

    Returns:
        Updated road section object or None if not found
    """
    road_section = get_road_section(db, road_section_id)
    if not road_section:
        return None

    # Update only provided fields
    update_data = road_section_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(road_section, field, value)

    db.commit()
    db.refresh(road_section)
    return road_section


def delete_road_section(db: Session, road_section_id: int) -> bool:
    """
    Delete a road section

    Args:
        db: Database session
        road_section_id: Road Section ID

    Returns:
        True if deleted, False if not found
    """
    road_section = get_road_section(db, road_section_id)
    if not road_section:
        return False

    db.delete(road_section)
    db.commit()
    return True
