"""
Orders API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.order import Order, OrderStatus, CargoType
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.services.safety_service import SafetyCheckService
from app.services.document_service import DocumentService

router = APIRouter()


@router.get("/", response_model=List[OrderResponse])
def get_orders(
    status: Optional[OrderStatus] = None,
    cargo_type: Optional[CargoType] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить список заказов с фильтрацией"""
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status)
    if cargo_type:
        query = query.filter(Order.cargo_type == cargo_type)
    
    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Создать новый заказ на перевозку"""
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Получить заказ по ID"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    """Обновить заказ"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    for field, value in order_update.dict(exclude_unset=True).items():
        setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    return order


@router.post("/{order_id}/safety-check")
def perform_safety_check(order_id: int, db: Session = Depends(get_db)):
    """Выполнить AI проверку безопасности груза"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    safety_service = SafetyCheckService()
    
    order_dict = {
        'id': order.id,
        'cargo_name': order.cargo_name,
        'cargo_type': order.cargo_type.value if order.cargo_type else 'general',
        'pickup_address': order.pickup_address,
        'delivery_address': order.delivery_address,
        'urgency_score': order.urgency_score,
        'weight_kg': order.weight_kg
    }
    
    result = safety_service.check_order_safety(order_dict)
    
    # Обновить заказ
    order.safety_checked = True
    order.safety_score = result.get('risk_score')
    order.safety_warnings = result.get('risk_factors', [])
    order.documents_required = result.get('required_documents', [])
    
    db.commit()
    
    return result


@router.get("/{order_id}/document-checklist")
def get_document_checklist(order_id: int, db: Session = Depends(get_db)):
    """Получить чеклист необходимых документов"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    doc_service = DocumentService()
    
    order_dict = {
        'id': order.id,
        'cargo_type': order.cargo_type.value if order.cargo_type else 'general',
        'pickup_address': order.pickup_address,
        'delivery_address': order.delivery_address
    }
    
    return doc_service.generate_document_checklist(order_dict)
