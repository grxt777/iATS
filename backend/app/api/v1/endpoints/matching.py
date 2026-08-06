"""
AI Matching API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.order import Order
from app.services.matching_service import SmartMatchingService
from app.schemas.matching import MatchingRequest, MatchingResponse

router = APIRouter()


@router.post("/", response_model=MatchingResponse)
def find_matching(request: MatchingRequest, db: Session = Depends(get_db)):
    """
    AI подбор лучшего транспорта для груза
    Использует ML модель + эвристики для оценки совместимости
    """
    # Получить заказ
    order = db.query(Order).filter(Order.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status.value != 'pending':
        raise HTTPException(
            status_code=400, 
            detail="Order must be in 'pending' status for matching"
        )
    
    # Подготовить данные для matching
    order_dict = {
        'id': order.id,
        'cargo_type': order.cargo_type.value if order.cargo_type else 'general',
        'cargo_name': order.cargo_name,
        'weight_kg': order.weight_kg,
        'volume_m3': order.volume_m3,
        'pickup_lat': order.pickup_lat,
        'pickup_lng': order.pickup_lng,
        'delivery_lat': order.delivery_lat,
        'delivery_lng': order.delivery_lng,
        'urgency_score': order.urgency_score,
        'budget_uzs': float(order.budget_uzs) if order.budget_uzs else None
    }
    
    # Выполнить matching
    matching_service = SmartMatchingService()
    result = matching_service.find_best_matches(db, order_dict, request.top_k)
    
    return result
