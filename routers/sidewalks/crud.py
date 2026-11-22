"""
Sidewalk CRUD operations
Database operations for sidewalks
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional
from .models import Sidewalk, SidewalkCondition
from .schemas import SidewalkCreate, SidewalkUpdate


def get_sidewalks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    condition: Optional[SidewalkCondition] = None,
    ada_compliant: Optional[bool] = None,
    surface_material: Optional[str] = None,
    search: Optional[str] = None
) -> tuple[list[Sidewalk], int]:
    """
    Get list of sidewalks with optional filtering

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        condition: Filter by condition rating
        ada_compliant: Filter by ADA compliance
        surface_material: Filter by surface material (case-insensitive exact match)
        search: Search term for street name or block number

    Returns:
        Tuple of (list of sidewalks, total count)
    """
    query = db.query(Sidewalk)

    # Apply filters
    if condition:
        query = query.filter(Sidewalk.condition == condition)

    if ada_compliant is not None:
        query = query.filter(Sidewalk.ada_compliant == ada_compliant)

    if surface_material:
        query = query.filter(
            func.lower(Sidewalk.surface_material) == surface_material.lower()
        )

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Sidewalk.street_name.ilike(search_term),
                Sidewalk.block_number.ilike(search_term)
            )
        )

    # Get total count before pagination
    total = query.count()

    # Apply pagination and get results
    sidewalks = query.offset(skip).limit(limit).all()

    return sidewalks, total


def get_sidewalk(db: Session, sidewalk_id: int) -> Optional[Sidewalk]:
    """
    Get a specific sidewalk by ID

    Args:
        db: Database session
        sidewalk_id: Sidewalk ID

    Returns:
        Sidewalk object or None if not found
    """
    return db.query(Sidewalk).filter(Sidewalk.id == sidewalk_id).first()


def create_sidewalk(db: Session, sidewalk_data: SidewalkCreate) -> Sidewalk:
    """
    Create a new sidewalk

    Args:
        db: Database session
        sidewalk_data: Sidewalk creation data

    Returns:
        Created sidewalk object
    """
    sidewalk = Sidewalk(**sidewalk_data.model_dump())
    db.add(sidewalk)
    db.commit()
    db.refresh(sidewalk)
    return sidewalk


def update_sidewalk(
    db: Session,
    sidewalk_id: int,
    sidewalk_data: SidewalkUpdate
) -> Optional[Sidewalk]:
    """
    Update an existing sidewalk

    Args:
        db: Database session
        sidewalk_id: Sidewalk ID
        sidewalk_data: Sidewalk update data

    Returns:
        Updated sidewalk object or None if not found
    """
    sidewalk = get_sidewalk(db, sidewalk_id)
    if not sidewalk:
        return None

    # Update only provided fields
    update_data = sidewalk_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sidewalk, field, value)

    db.commit()
    db.refresh(sidewalk)
    return sidewalk


def delete_sidewalk(db: Session, sidewalk_id: int) -> bool:
    """
    Delete a sidewalk

    Args:
        db: Database session
        sidewalk_id: Sidewalk ID

    Returns:
        True if deleted, False if not found
    """
    sidewalk = get_sidewalk(db, sidewalk_id)
    if not sidewalk:
        return False

    db.delete(sidewalk)
    db.commit()
    return True
