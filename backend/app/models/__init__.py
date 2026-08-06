"""
Database Models - ORM Definitions
"""
from app.models.user import User
from app.models.order import Order
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.document import Document, DocumentType
from app.models.route import Route, RouteSegment
from app.models.permit import Permit, PermitType
from app.models.matching import MatchingResult
from app.models.safety_check import SafetyCheck

__all__ = [
    "User",
    "Order",
    "Vehicle", 
    "Driver",
    "Document",
    "DocumentType",
    "Route",
    "RouteSegment",
    "Permit",
    "PermitType",
    "MatchingResult",
    "SafetyCheck"
]
