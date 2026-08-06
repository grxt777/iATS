"""
Matching Result Model - Результаты AI подбора
"""
from sqlalchemy import (Column, Integer, String, Float, Boolean, DateTime,
                        ForeignKey, Text, JSON)
from sqlalchemy.sql import func
from app.core.database import Base


class MatchingResult(Base):
    __tablename__ = "matching_results"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    
    # AI Score
    overall_score = Column(Float, nullable=False)  # 0-100
    confidence = Column(String, nullable=True)     # high, medium, low
    
    # Score breakdown
    distance_score = Column(Float, nullable=True)      # Proximity to pickup
    capacity_score = Column(Float, nullable=True)      # Capacity utilization
    rating_score = Column(Float, nullable=True)        # Driver/vehicle rating
    price_score = Column(Float, nullable=True)         # Budget compatibility
    history_score = Column(Float, nullable=True)       # Historical performance
    permit_score = Column(Float, nullable=True)        # Permit compatibility
    
    # Features used
    features = Column(JSON, nullable=True)  # All features used for scoring
    
    # Ranking
    rank = Column(Integer, nullable=True)  # Position in results (1=best)
    
    # Status
    is_accepted = Column(Boolean, default=False)
    accepted_at = Column(DateTime, nullable=True)
    
    # Explanation
    explanation = Column(Text, nullable=True)  # Why this match is good
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
