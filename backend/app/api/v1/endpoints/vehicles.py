"""
Vehicles API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.vehicle import Vehicle, VehicleStatus, VehicleType
from app.schemas.vehicle import VehicleCreate, VehicleResponse

router = APIRouter()


@router.get("/", response_model=List[VehicleResponse])
def get_vehicles(
    status: Optional[VehicleStatus] = None,
    vehicle_type: Optional[VehicleType] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить список доступного транспорта"""
    query = db.query(Vehicle)
    
    if status:
        query = query.filter(Vehicle.status == status)
    if vehicle_type:
        query = query.filter(Vehicle.type == vehicle_type)
    
    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=VehicleResponse)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """Добавить новый транспорт"""
    db_vehicle = Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Получить транспорт по ID"""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle
