"""
Order Model - Груз/Заявка на перевозку
"""
from sqlalchemy import (Column, Integer, String, Float, Boolean, DateTime, 
                        ForeignKey, Enum, Text, JSON, Numeric)
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class OrderStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    MATCHED = "matched"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class CargoType(str, enum.Enum):
    GENERAL = "general"                # Обычный груз
    PERISHABLE = "perishable"          # Скоропортящийся
    DANGEROUS = "dangerous"            # Опасный (ADR)
    OVERSIZED = "oversized"            # Крупногабаритный
    VALUABLE = "valuable"              # Ценный
    LIVE_ANIMALS = "live_animals"      # Живые животные
    REFRIGERATED = "refrigerated"      # Рефрижераторный


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Shipper info
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Cargo details
    cargo_type = Column(Enum(CargoType), default=CargoType.GENERAL)
    cargo_name = Column(String, nullable=False)
    cargo_description = Column(Text, nullable=True)
    weight_kg = Column(Float, nullable=False)
    volume_m3 = Column(Float, nullable=True)
    adr_class = Column(Integer, nullable=True)  # 1-9 для опасных грузов
    adr_subclass = Column(String, nullable=True)
    
    # Route
    pickup_address = Column(String, nullable=False)
    pickup_lat = Column(Float, nullable=False)
    pickup_lng = Column(Float, nullable=False)
    delivery_address = Column(String, nullable=False)
    delivery_lat = Column(Float, nullable=False)
    delivery_lng = Column(Float, nullable=False)
    
    # Timing
    pickup_date = Column(DateTime, nullable=False)
    delivery_deadline = Column(DateTime, nullable=True)
    urgency_score = Column(Integer, default=5)  # 1-10
    
    # Financial
    budget_uzs = Column(Numeric(precision=12, scale=2), nullable=True)
    price_negotiable = Column(Boolean, default=True)
    
    # Status & Matching
    status = Column(Enum(OrderStatus), default=OrderStatus.DRAFT)
    matched_vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    matching_score = Column(Float, nullable=True)  # 0-100
    
    # Safety check
    safety_checked = Column(Boolean, default=False)
    safety_score = Column(Float, nullable=True)  # 0-100
    safety_warnings = Column(JSON, nullable=True)  # List of warnings
    
    # Documents
    documents_required = Column(JSON, nullable=True)  # List of required docs
    documents_uploaded = Column(JSON, nullable=True)  # List of uploaded docs
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    # vehicle = relationship("Vehicle", back_populates="current_order")
