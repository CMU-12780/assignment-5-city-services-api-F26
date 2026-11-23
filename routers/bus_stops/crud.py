from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional
from .models import BusStops
from .schemas import BusStopCreate, BusStopUpdate

def get_BusStops(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        id_num: Optional[str] = None,
        routes: Optional[str] = None,
        search: Optional[str] = None
) -> tuple[list[BusStops], int]:
    '''
    Get a list of bus stops with optional filtering
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maxmimum number of records to return
        id_num: Search for bus stop by id number
        routes: Search for bus stop by line
        search: Search term for location
        
    Returns:
        Tuple of (list of bus stops, total count)
    '''
    query = db.query(BusStops)

    if id_num:
        search_term = f'%{search}%'
        query = query.filter(
            BusStops.stop_id.ilike(search_term)
        )

    if search:
       search_term = f"%{search}%"
       query = query.filter(
           BusStops.location.ilike(search_term)
           )

    if routes:
        clean_search = search.strip()
        exact_route = f"%.{clean_search},%"

        padded_column = func.concat(",", func.replace(BusStops.routes_served," ",""),",")
        query = query.filter(padded_column.ilike(exact_route))

    total = query.count()

    bus_stops = query.offset(skip).limit(limit).all()

    return bus_stops, total

def get_BusStop(db: Session, bus_stop_id: int) -> Optional[BusStops]:
    '''
    Get a specific bridge by ID
    
    Args:
        db: Database session
        bus_stop_id: Bus Stop ID
        
    Returns:
        Bus Stop Object or None if not found
    '''

    return db.query(BusStops).filter(BusStops.id == bus_stop_id).first()

def create_BusStop(db: Session, bus_stop_data: BusStopCreate) -> BusStops:

    '''
    Create a new bus stop
    
    Args:
        db: Database Session
        bus_stop_data: Bus Stop creation data
        
    Returns:
        Created bus stop object
    '''

    bus_stop = BusStops(**bus_stop_data.model_dump())
    db.add(bus_stop)
    db.commit()
    db.refrech(bus_stop)
    return bus_stop


def update_BusStop(db: Session,
                    bus_stop_id: int,
                    bus_stop_data: BusStopUpdate
                    ) -> Optional[BusStops]:
    '''
    Update an Existing Bus Stop
    
    Args:
        db: Database Session
        bus_stop_id: Bus Stop ID
        bus_stop_data: Bus Update Data
        
    Returns:
        Updated Bus Stop object or None if not found
    '''

    bus_stop = get_BusStops(db,bus_stop_id)
    if not bus_stop:
        return None

    update_data = bus_stop_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bus_stop, field, value)

    db.commit
    db.refresh(bus_stop)
    return bus_stop
    

def delete_resource(db: Session, bus_stop_id: int) -> bool:

    '''
    Delete a bus stop
    
    Args:
        db: Database session
        bus_stop_id: Bus Stop ID
            
    Returns:
       True if deleted, False if not found
    '''

    bus_stop = get_BusStops(db, bus_stop_id)
    if not bus_stop:
        return False

    db.delete(bus_stop)
    db.commit()
    return True

    