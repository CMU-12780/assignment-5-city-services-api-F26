from sqlalchemy.orm import Session
from .models import AirQualitySensor
from .schemas import AirQualitySensorCreate, AirQualitySensorUpdate
# crud code for air quality sensors

def get_sensors(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(AirQualitySensor)
    total = query.count()
    sensors = query.offset(skip).limit(limit).all()
    return sensors, total


def get_sensor(db: Session, sensor_id: int):
    return db.query(AirQualitySensor).filter(AirQualitySensor.id == sensor_id).first()


def create_sensor(db: Session, sensor_data: AirQualitySensorCreate):
    sensor = AirQualitySensor(**sensor_data.model_dump())
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return sensor


def update_sensor(db: Session, sensor_id: int, sensor_data: AirQualitySensorUpdate):
    sensor = get_sensor(db, sensor_id)
    if not sensor:
        return None
    for field, value in sensor_data.model_dump(exclude_unset=True).items():
        setattr(sensor, field, value)
    db.commit()
    db.refresh(sensor)
    return sensor


def delete_sensor(db: Session, sensor_id: int):
    sensor = get_sensor(db, sensor_id)
    if not sensor:
        return False
    db.delete(sensor)
    db.commit()
    return True