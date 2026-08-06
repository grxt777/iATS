"""
Vehicle Model - Транспортное средство
"""
from sqlalchemy import (Column, Integer, String, Float, Boolean, DateTime,
                        ForeignKey, Enum, Numeric, Text)
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class VehicleType(str, enum.Enum):
    VAN = "van"                      # Фургон (до 1.5т)
    TRUCK_SMALL = "truck_small"      # Малый грузовик (до 5т)
    TRUCK_MEDIUM = "truck_medium"    # Средний (до 10т)
    TRUCK_LARGE = "truck_large"      # Большой (до 20т)
    TRUCK_JUMBO = "truck_jumbo"      # Джамбо (до 25т)
    TANKER = "tanker"                # Танкер
    REFRIGERATOR = "refrigerator"    # Рефрижератор
    FLATBED = "flatbed"              # Бортовой/Платформа
    CONTAINER = "container"          # Контейнеровоз


class VehicleStatus(str, enum.Enum):
    AVAILABLE = "available"
    IN_TRANSIT = "in_transit"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Owner
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    
    # Vehicle details
    type = Column(Enum(VehicleType), nullable=False)
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    license_plate = Column(String, nullable=False, unique=True)
    vin = Column(String, nullable=True)
    
    # Capacity
    capacity_kg = Column(Float, nullable=False)
    volume_m3 = Column(Float, nullable=True)
    length_m = Column(Float, nullable=True)
    width_m = Column(Float, nullable=True)
    height_m = Column(Float, nullable=True)
    
    # Location (current)
    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    current_address = Column(String, nullable=True)
    
    # Status
    status = Column(Enum(VehicleStatus), default=VehicleStatus.AVAILABLE)
    
    # Financial
    cost_per_km_uzs = Column(Numeric(precision=8, scale=2), nullable=True)
    min_order_value_uzs = Column(Numeric(precision=10, scale=2), nullable=True)
    
    # Permits & Certifications
    has_international_permit = Column(Boolean, default=False)
    permit_countries = Column(Text, nullable=True)  # JSON list of country codes
    has_dangerous_goods_permit = Column(Boolean, default=False)
    adr_classes_allowed = Column(Text, nullable=True)  # JSON list
    license_expiry = Column(DateTime, nullable=True)
    
    # Performance metrics
    total_trips = Column(Integer, default=0)
    successful_trips = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)  # 0-1
    average_rating = Column(Float, default=5.0)  # 0-5
    total_revenue_uzs = Column(Numeric(precision=12, scale=2), default=0)
    
    # Profitability coefficient (for permit allocation)
    profitability_coefficient = Column(Float, default=1.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
