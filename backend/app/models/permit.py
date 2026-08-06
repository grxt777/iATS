"""
Permit Models - Рухсатнома (Разрешения на международные перевозки)
"""
from sqlalchemy import (Column, Integer, String, Boolean, DateTime,
                        ForeignKey, Enum, Text, Float, Date)
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class PermitType(str, enum.Enum):
    BILATERAL = "bilateral"           # Двусторонние перевозки
    TRANSIT = "transit"               # Транзитные перевозки
    THIRD_COUNTRY = "third_country"   # Перевозки в/из третьих стран


class PermitStatus(str, enum.Enum):
    AVAILABLE = "available"           # Доступно
    RESERVED = "reserved"             # Забронировано
    ISSUED = "issued"                 # Выдано
    IN_USE = "in_use"                 # Используется
    RETURNED = "returned"             # Возвращено
    EXPIRED = "expired"               # Истекло


class Permit(Base):
    __tablename__ = "permits"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Type & Country
    permit_type = Column(Enum(PermitType), nullable=False)
    country_code = Column(String, nullable=False)  # ISO country code (RU, KZ, CN, etc.)
    country_name = Column(String, nullable=False)
    
    # Status
    status = Column(Enum(PermitStatus), default=PermitStatus.AVAILABLE)
    
    # Allocation
    carrier_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    
    # Validity
    issued_date = Column(Date, nullable=True)
    valid_until = Column(Date, nullable=True)  # Must return within 90 days
    return_date = Column(Date, nullable=True)
    
    # Route
    route_from = Column(String, nullable=True)
    route_to = Column(String, nullable=True)
    
    # Quota info
    quota_year = Column(Integer, nullable=True)
    is_from_exchange_quota = Column(Boolean, default=True)
    
    # Cost
    fee_uzs = Column(Integer, default=82500)  # 1/4 БРВ
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PermitQuota(Base):
    __tablename__ = "permit_quotas"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Quota details
    country_code = Column(String, nullable=False)
    country_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    permit_type = Column(Enum(PermitType), nullable=False)
    
    # Numbers
    total_quota = Column(Integer, nullable=False)
    distributed = Column(Integer, default=0)
    available = Column(Integer, default=0)
    reserved = Column(Integer, default=0)
    used = Column(Integer, default=0)
    returned = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_deficit = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
