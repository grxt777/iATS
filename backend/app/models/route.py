"""
Route Models - Маршруты
"""
from sqlalchemy import (Column, Integer, String, Float, Boolean, DateTime,
                        ForeignKey, Enum, Text, JSON, Numeric)
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class RouteStatus(str, enum.Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RouteValidationStatus(str, enum.Enum):
    VALID = "valid"                # Маршрут подходит
    WARNING = "warning"            # Есть предупреждения
    INVALID = "invalid"            # Маршрут не подходит
    NEEDS_REVIEW = "needs_review"  # Требует ручной проверки


class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    
    # Route geometry
    route_geometry = Column(JSON, nullable=True)  # GeoJSON LineString
    route_points = Column(JSON, nullable=True)    # List of lat/lng points
    
    # Distance & Time
    total_distance_km = Column(Float, nullable=True)
    estimated_duration_min = Column(Integer, nullable=True)
    actual_duration_min = Column(Integer, nullable=True)
    
    # Costs
    estimated_fuel_cost_uzs = Column(Numeric(precision=10, scale=2), nullable=True)
    estimated_toll_cost_uzs = Column(Numeric(precision=10, scale=2), nullable=True)
    estimated_total_cost_uzs = Column(Numeric(precision=10, scale=2), nullable=True)
    
    # Validation
    validation_status = Column(
        Enum(RouteValidationStatus), 
        default=RouteValidationStatus.VALID
    )
    validation_issues = Column(JSON, nullable=True)  # List of issues found
    rejected_segments = Column(JSON, nullable=True)  # Segments that were rejected
    
    # Alternative routes
    is_alternative = Column(Boolean, default=False)
    alternative_rank = Column(Integer, nullable=True)  # 1=best, 2, 3...
    
    # Status
    status = Column(Enum(RouteStatus), default=RouteStatus.PLANNED)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class RouteSegment(Base):
    __tablename__ = "route_segments"
    
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    
    # Segment info
    segment_index = Column(Integer, nullable=False)
    start_lat = Column(Float, nullable=False)
    start_lng = Column(Float, nullable=False)
    end_lat = Column(Float, nullable=False)
    end_lng = Column(Float, nullable=False)
    
    # Segment properties
    distance_km = Column(Float, nullable=True)
    duration_min = Column(Integer, nullable=True)
    road_type = Column(String, nullable=True)  # highway, urban, rural, etc.
    speed_limit = Column(Integer, nullable=True)
    
    # Restrictions
    max_weight_tons = Column(Float, nullable=True)
    max_height_m = Column(Float, nullable=True)
    max_width_m = Column(Float, nullable=True)
    max_length_m = Column(Float, nullable=True)
    
    # Hazards & Restrictions
    has_tunnel = Column(Boolean, default=False)
    has_bridge = Column(Boolean, default=False)
    is_residential_zone = Column(Boolean, default=False)
    has_dangerous_goods_restriction = Column(Boolean, default=False)
    restriction_details = Column(Text, nullable=True)  # JSON
    
    # Weather impact
    weather_condition = Column(String, nullable=True)
    weather_impact_score = Column(Float, nullable=True)  # 0-1, higher=worse
    
    # Validation
    is_valid = Column(Boolean, default=True)
    validation_issues = Column(JSON, nullable=True)
