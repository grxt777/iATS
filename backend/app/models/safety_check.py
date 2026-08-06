"""
Safety Check Model - Проверка безопасности груза
"""
from sqlalchemy import (Column, Integer, String, Float, Boolean, DateTime,
                        ForeignKey, Text, JSON)
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class CargoRiskLevel(str, enum.Enum):
    LOW = "low"           # Низкий риск
    MEDIUM = "medium"     # Средний риск
    HIGH = "high"         # Высокий риск
    CRITICAL = "critical" # Критический риск


class SafetyCheckStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    NEEDS_REVIEW = "needs_review"


class SafetyCheck(Base):
    __tablename__ = "safety_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    
    # Cargo classification
    cargo_name = Column(String, nullable=False)
    detected_cargo_type = Column(String, nullable=True)
    is_perishable = Column(Boolean, default=False)
    is_dangerous = Column(Boolean, default=False)
    adr_class = Column(Integer, nullable=True)
    adr_class_name = Column(String, nullable=True)
    un_number = Column(String, nullable=True)  # UN number for dangerous goods
    
    # Risk assessment
    risk_level = Column(Enum(CargoRiskLevel), default=CargoRiskLevel.LOW)
    risk_score = Column(Integer, default=0)  # 0-100
    risk_factors = Column(JSON, nullable=True)  # List of risk factors
    
    # Required documents
    required_documents = Column(JSON, nullable=True)  # List of required doc types
    documents_provided = Column(JSON, nullable=True)  # List of provided docs
    documents_missing = Column(JSON, nullable=True)   # List of missing docs
    documents_valid = Column(JSON, nullable=True)     # Validation results
    
    # Route restrictions
    route_restrictions = Column(JSON, nullable=True)  # Restrictions for this cargo
    forbidden_segments = Column(JSON, nullable=True)  # Route segments to avoid
    special_requirements = Column(JSON, nullable=True)  # Special handling needs
    
    # AI Analysis
    ai_model_used = Column(String, nullable=True)
    ai_confidence = Column(Float, nullable=True)
    ai_analysis = Column(Text, nullable=True)
    
    # Status
    status = Column(Enum(SafetyCheckStatus), default=SafetyCheckStatus.PENDING)
    notes = Column(Text, nullable=True)
    
    # Performed by
    performed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
