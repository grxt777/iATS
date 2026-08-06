"""
Matching Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class MatchingRequest(BaseModel):
    order_id: int
    top_k: int = Field(5, ge=1, le=20)


class MatchingResultItem(BaseModel):
    vehicle_id: int
    rank: int
    overall_score: float
    confidence: str
    
    distance_score: float
    capacity_score: float
    rating_score: float
    price_score: float
    history_score: float
    permit_score: float
    
    driver_name: Optional[str] = None
    vehicle_type: Optional[str] = None
    license_plate: Optional[str] = None
    current_distance_km: Optional[float] = None
    estimated_cost_uzs: Optional[float] = None
    
    explanation: Optional[str] = None


class MatchingResponse(BaseModel):
    order_id: int
    results: List[MatchingResultItem]
    total_vehicles_evaluated: int
    processing_time_ms: float
