"""
User Model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class UserRole(str, enum.Enum):
    SHIPPER = "shipper"          # Грузоотправитель
    CARRIER = "carrier"          # Перевозчик
    DRIVER = "driver"            # Водитель
    ADMIN = "admin"              # Администратор
    INSPECTOR = "inspector"      # Инспектор


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    inn = Column(String, nullable=True)  # Идентификационный номер налогоплательщика
    role = Column(Enum(UserRole), default=UserRole.SHIPPER, nullable=False)
    
    # Verification
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships (defined in other models)
    # orders = relationship("Order", back_populates="user")
    # vehicles = relationship("Vehicle", back_populates="owner")
