"""
Document Models - Документы для перевозки
"""
from sqlalchemy import (Column, Integer, String, Boolean, DateTime,
                        ForeignKey, Enum, Text, Float)
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class DocumentType(str, enum.Enum):
    # Basic documents
    ETTN = "ettn"                          # Электронная ТТН
    WAYBILL = "waybill"                    # Путевой лист
    LICENSE = "license"                    # Лицензия перевозчика
    
    # Cargo specific
    PHYTOSANITARY = "phytosanitary"        # Фитосанитарный сертификат
    VETERINARY = "veterinary"              # Ветеринарный сертификат
    SANITARY = "sanitary"                  # Санитарное заключение
    CERTIFICATE_OF_CONFORMITY = "coc"      # Сертификат соответствия
    ORIGIN_CERTIFICATE = "origin_cert"     # Сертификат происхождения (СТ-1)
    
    # Dangerous goods
    ADR_CERTIFICATE = "adr_cert"           # ДОПОГ свидетельство
    DANGEROUS_GOODS_PERMIT = "dg_permit"   # Разрешение на перевозку ОГ
    EMERGENCY_CARD = "emergency_card"      # Аварийная карточка
    
    # International
    CMR = "cmr"                            # Международная накладная
    CUSTOMS_DECLARATION = "customs_decl"   # Таможенная декларация (ГТД)
    PERMIT = "permit"                      # Рухсатнома
    
    # Other
    INSURANCE = "insurance"                # Страховка
    INVOICE = "invoice"                    # Инвойс
    PACKING_LIST = "packing_list"          # Упаковочный лист
    CONTRACT = "contract"                  # Контракт


class DocumentStatus(str, enum.Enum):
    PENDING = "pending"         # Ожидает загрузки
    UPLOADED = "uploaded"       # Загружен
    VERIFYING = "verifying"     # На проверке (AI)
    VERIFIED = "verified"       # Проверен
    REJECTED = "rejected"       # Отклонён
    EXPIRED = "expired"         # Истёк срок


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Link to order or vehicle
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    
    # Document info
    doc_type = Column(Enum(DocumentType), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # File
    file_path = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    file_mime_type = Column(String, nullable=True)
    
    # AI Analysis
    ai_extracted_data = Column(Text, nullable=True)  # JSON with extracted fields
    ai_confidence = Column(Float, nullable=True)     # 0-1
    ai_validation_result = Column(String, nullable=True)  # "valid", "invalid", "warning"
    ai_warnings = Column(Text, nullable=True)        # JSON list of warnings
    
    # Status
    status = Column(Enum(DocumentStatus), default=DocumentStatus.PENDING)
    rejection_reason = Column(Text, nullable=True)
    
    # Validity
    issue_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    is_expired = Column(Boolean, default=False)
    
    # Verification
    verified_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
