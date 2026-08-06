"""
Safety Check Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class SafetyCheckRequest(BaseModel):
    order_id: int


class SafetyCheckResult(BaseModel):
    order_id: int
    cargo_name: str
    detected_cargo_type: str
    
    is_perishable: bool
    is_dangerous: bool
    adr_class: Optional[int] = None
    adr_class_name: Optional[str] = None
    un_number: Optional[str] = None
    
    risk_level: str
    risk_score: int
    risk_factors: List[str]
    
    required_documents: List[str]
    documents_provided: List[str]
    documents_missing: List[str]
    documents_valid: Dict[str, bool]
    
    route_restrictions: List[str]
    forbidden_segments: List[Dict[str, Any]]
    special_requirements: List[str]
    
    ai_confidence: float
    status: str
    notes: Optional[str] = None


class DocumentVerificationRequest(BaseModel):
    document_id: int


class DocumentVerificationResult(BaseModel):
    document_id: int
    is_valid: bool
    extracted_data: Dict[str, Any]
    confidence: float
    warnings: List[str]
    expiry_date: Optional[str] = None
    is_expired: bool
