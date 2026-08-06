"""
Vehicle Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.vehicle import VehicleType, VehicleStatus


class VehicleCreate(BaseModel):
    type: VehicleType
    brand: Optional[str] = None
    model: Optional[str] = None
    license_plate: str = Field(..., min_length=1)
    vin: Optional[str] = None
    
    capacity_kg: float = Field(..., gt=0)
    volume_m3: Optional[float] = Field(None, gt=0)
    length_m: Optional[float] = None
    width_m: Optional[float] = None
    height_m: Optional[float] = None
    
    cost_per_km_uzs: Optional[float] = None
    min_order_value_uzs: Optional[float] = None
    
    has_international_permit: bool = False
    permit_countries: Optional[List[str]] = None
    has_dangerous_goods_permit: bool = False
    adr_classes_allowed: Optional[List[int]] = None


class VehicleResponse(BaseModel):
    id: int
    owner_id: int
    driver_id: Optional[int]
    
    type: VehicleType
    brand: Optional[str]
    model: Optional[str]
    license_plate: str
    vin: Optional[str]
    
    capacity_kg: float
    volume_m3: Optional[float]
    length_m: Optional[float]
    width_m: Optional[float]
    height_m: Optional[float]
    
    current_lat: Optional[float]
    current_lng: Optional[float]
    current_address: Optional[str]
    
    status: VehicleStatus
    
    cost_per_km_uzs: Optional[float]
    
    has_international_permit: bool
    permit_countries: Optional[List[str]]
    has_dangerous_goods_permit: bool
    adr_classes_allowed: Optional[List[int]]
    
    total_trips: int
    successful_trips: int
    success_rate: float
    average_rating: float
    
    profitability_coefficient: float
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
