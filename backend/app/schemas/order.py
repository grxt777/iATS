"""
Order Schemas - Pydantic Models for Orders
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.order import OrderStatus, CargoType


class OrderCreate(BaseModel):
    cargo_type: CargoType = CargoType.GENERAL
    cargo_name: str = Field(..., min_length=1, max_length=200)
    cargo_description: Optional[str] = None
    weight_kg: float = Field(..., gt=0)
    volume_m3: Optional[float] = Field(None, gt=0)
    adr_class: Optional[int] = Field(None, ge=1, le=9)
    adr_subclass: Optional[str] = None
    
    pickup_address: str
    pickup_lat: float
    pickup_lng: float
    delivery_address: str
    delivery_lat: float
    delivery_lng: float
    
    pickup_date: datetime
    delivery_deadline: Optional[datetime] = None
    urgency_score: int = Field(5, ge=1, le=10)
    
    budget_uzs: Optional[float] = None
    price_negotiable: bool = True


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    matched_vehicle_id: Optional[int] = None
    budget_uzs: Optional[float] = None
    delivery_deadline: Optional[datetime] = None


class OrderResponse(BaseModel):
    id: int
    user_id: int
    
    cargo_type: CargoType
    cargo_name: str
    cargo_description: Optional[str]
    weight_kg: float
    volume_m3: Optional[float]
    adr_class: Optional[int]
    adr_subclass: Optional[str]
    
    pickup_address: str
    pickup_lat: float
    pickup_lng: float
    delivery_address: str
    delivery_lat: float
    delivery_lng: float
    
    pickup_date: datetime
    delivery_deadline: Optional[datetime]
    urgency_score: int
    
    budget_uzs: Optional[float]
    price_negotiable: bool
    
    status: OrderStatus
    matched_vehicle_id: Optional[int]
    matching_score: Optional[float]
    
    safety_checked: bool
    safety_score: Optional[float]
    safety_warnings: Optional[List[str]]
    
    documents_required: Optional[List[str]]
    documents_uploaded: Optional[List[str]]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
