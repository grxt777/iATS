"""
Routing Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class RouteRequest(BaseModel):
    order_id: int
    vehicle_id: int
    consider_weather: bool = True
    consider_restrictions: bool = True
    alternatives_count: int = Field(2, ge=0, le=5)


class RouteSegmentInfo(BaseModel):
    segment_index: int
    start_lat: float
    start_lng: float
    end_lat: float
    end_lng: float
    distance_km: float
    duration_min: int
    road_type: str
    speed_limit: Optional[int] = None
    
    max_weight_tons: Optional[float] = None
    max_height_m: Optional[float] = None
    
    has_tunnel: bool
    has_bridge: bool
    is_residential_zone: bool
    has_dangerous_goods_restriction: bool
    restriction_details: Optional[str] = None
    
    weather_condition: Optional[str] = None
    weather_impact_score: Optional[float] = None
    
    is_valid: bool
    validation_issues: Optional[List[str]] = None


class RouteInfo(BaseModel):
    route_id: int
    total_distance_km: float
    estimated_duration_min: int
    
    estimated_fuel_cost_uzs: float
    estimated_toll_cost_uzs: float
    estimated_total_cost_uzs: float
    
    validation_status: str
    validation_issues: Optional[List[str]] = None
    
    segments: List[RouteSegmentInfo]
    
    is_alternative: bool
    alternative_rank: Optional[int] = None
    
    notes: Optional[str] = None


class RouteResponse(BaseModel):
    order_id: int
    vehicle_id: int
    routes: List[RouteInfo]
    recommended_route_id: int
    processing_time_ms: float
