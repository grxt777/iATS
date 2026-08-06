"""
Driver Model - Водитель
"""
from sqlalchemy import (Column, Integer, String, Boolean, DateTime,
                        ForeignKey, Date, Text)
from sqlalchemy.sql import func
from app.core.database import Base


class Driver(Base):
    __tablename__ = "drivers"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal info
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String, nullable=False)
    pinfl = Column(String, nullable=False, unique=True)  # Personal ID
    phone = Column(String, nullable=False)
    
    # License
    license_number = Column(String, nullable=False)
    license_category = Column(String, nullable=True)  # B, C, CE, etc.
    license_issue_date = Column(Date, nullable=True)
    license_expiry_date = Column(Date, nullable=True)
    
    # Experience
    experience_years = Column(Integer, default=0)
    
    # Certifications
    has_adr_certificate = Column(Boolean, default=False)
    adr_expiry_date = Column(Date, nullable=True)
    has_medical_certificate = Column(Boolean, default=False)
    medical_expiry_date = Column(Date, nullable=True)
    
    # Performance
    total_trips = Column(Integer, default=0)
    safe_trips = Column(Integer, default=0)
    safety_score = Column(Integer, default=100)  # 0-100
    violations_count = Column(Integer, default=0)
    average_rating = Column(Float, default=5.0)
    
    # Status
    is_available = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
