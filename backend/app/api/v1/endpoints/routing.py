"""
AI Routing API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.order import Order
from app.models.vehicle import Vehicle
from app.services.routing_service import RouteValidationService
from app.services.safety_service import SafetyCheckService
from app.schemas.routing import RouteRequest, RouteResponse

router = APIRouter()


@router.post("/", response_model=RouteResponse)
async def build_route(request: RouteRequest, db: Session = Depends(get_db)):
    """
    Построить и валидировать маршрут с учётом ограничений груза
    Интеграция с Yandex Routing API + OpenRouteService + OpenWeatherMap
    """
    # Получить заказ и транспорт
    order = db.query(Order).filter(Order.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    vehicle = db.query(Vehicle).filter(Vehicle.id == request.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # Получить safety check для ограничений
    safety_service = SafetyCheckService()
    safety_check = None
    if order.safety_checked:
        safety_check = {
            'adr_class': order.adr_class,
            'is_dangerous': order.cargo_type.value == 'dangerous' if order.cargo_type else False,
            'is_perishable': order.cargo_type.value == 'perishable' if order.cargo_type else False
        }
    
    # Подготовить данные
    order_dict = {
        'id': order.id,
        'pickup_lat': order.pickup_lat,
        'pickup_lng': order.pickup_lng,
        'delivery_lat': order.delivery_lat,
        'delivery_lng': order.delivery_lng,
        'cargo_name': order.cargo_name
    }
    
    vehicle_dict = {
        'id': vehicle.id,
        'type': vehicle.type.value if vehicle.type else 'truck_medium',
        'capacity_kg': vehicle.capacity_kg
    }
    
    # Построить маршрут
    routing_service = RouteValidationService()
    result = await routing_service.build_and_validate_route(
        order_dict,
        vehicle_dict,
        safety_check,
        request.alternatives_count
    )
    
    return result
