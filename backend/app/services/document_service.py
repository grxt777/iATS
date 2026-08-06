"""
Document Management Service
Управление документами для перевозки
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from loguru import logger


class DocumentService:
    """
    Сервис управления документами
    Автоматически определяет необходимые документы для груза
    """
    
    # Справочник документов и их требований
    DOCUMENT_REQUIREMENTS = {
        'ettn': {
            'name': 'Электронная ТТН',
            'required_for': ['all'],
            'validity_days': None,  # Действует на одну поездку
            'issuing_authority': 'Система ЭТТН'
        },
        'waybill': {
            'name': 'Путевой лист',
            'required_for': ['all'],
            'validity_days': 1,
            'issuing_authority': 'Оператор ИС ЭПД'
        },
        'license': {
            'name': 'Лицензия перевозчика',
            'required_for': ['all'],
            'validity_days': 365,
            'issuing_authority': 'Минтранс / Центры госуслуг'
        },
        'phytosanitary': {
            'name': 'Фитосанитарный сертификат',
            'required_for': ['perishable', 'plants'],
            'validity_days': 15,  # 14 дней для ЕС, 15 для других
            'issuing_authority': 'Агентство по карантину растений'
        },
        'veterinary': {
            'name': 'Ветеринарный сертификат',
            'required_for': ['animals', 'animal_products'],
            'validity_days': 5,
            'issuing_authority': 'Ветеринарная инспекция'
        },
        'sanitary': {
            'name': 'Санитарное заключение',
            'required_for': ['perishable', 'food'],
            'validity_days': 90,
            'issuing_authority': 'СЭС'
        },
        'coc': {
            'name': 'Сертификат соответствия',
            'required_for': ['regulated_goods'],
            'validity_days': 365,
            'issuing_authority': 'Узстандарт'
        },
        'origin_cert': {
            'name': 'Сертификат происхождения (СТ-1)',
            'required_for': ['international'],
            'validity_days': 120,
            'issuing_authority': 'Торгово-промышленная палата'
        },
        'adr_cert': {
            'name': 'Свидетельство ДОПОГ',
            'required_for': ['dangerous'],
            'validity_days': 365,
            'issuing_authority': 'Минтранс'
        },
        'dg_permit': {
            'name': 'Разрешение на перевозку ОГ',
            'required_for': ['dangerous'],
            'validity_days': 30,
            'issuing_authority': 'Минтранс'
        },
        'emergency_card': {
            'name': 'Аварийная карточка',
            'required_for': ['dangerous'],
            'validity_days': None,
            'issuing_authority': 'Перевозчик'
        },
        'cmr': {
            'name': 'Международная накладная CMR',
            'required_for': ['international'],
            'validity_days': None,
            'issuing_authority': 'Перевозчик'
        },
        'customs_decl': {
            'name': 'Таможенная декларация (ГТД)',
            'required_for': ['international'],
            'validity_days': None,
            'issuing_authority': 'Государственный таможенный комитет'
        },
        'permit': {
            'name': 'Рухсатнома',
            'required_for': ['international'],
            'validity_days': 90,  # Должен быть возвращён в течение 90 дней
            'issuing_authority': 'АИС Е-авто рухсатнома'
        },
        'insurance': {
            'name': 'Страховка груза',
            'required_for': ['valuable', 'dangerous'],
            'validity_days': 365,
            'issuing_authority': 'Страховая компания'
        }
    }
    
    def get_required_documents(
        self,
        cargo_type: str,
        is_international: bool = False,
        cargo_name: Optional[str] = None
    ) -> List[Dict]:
        """
        Определить список необходимых документов для перевозки
        """
        required = []
        
        for doc_type, doc_info in self.DOCUMENT_REQUIREMENTS.items():
            if 'all' in doc_info['required_for']:
                required.append({
                    'type': doc_type,
                    'name': doc_info['name'],
                    'required': True,
                    'issuing_authority': doc_info['issuing_authority'],
                    'validity_days': doc_info['validity_days']
                })
            
            if cargo_type in doc_info['required_for']:
                required.append({
                    'type': doc_type,
                    'name': doc_info['name'],
                    'required': True,
                    'issuing_authority': doc_info['issuing_authority'],
                    'validity_days': doc_info['validity_days']
                })
            
            if is_international and 'international' in doc_info['required_for']:
                # Избегаем дубликатов
                if not any(r['type'] == doc_type for r in required):
                    required.append({
                        'type': doc_type,
                        'name': doc_info['name'],
                        'required': True,
                        'issuing_authority': doc_info['issuing_authority'],
                        'validity_days': doc_info['validity_days']
                    })
        
        return required
    
    def check_document_validity(self, document: Dict) -> Dict:
        """
        Проверить действительность документа
        """
        doc_type = document.get('type')
        expiry_date = document.get('expiry_date')
        
        if not doc_type:
            return {'valid': False, 'reason': 'Тип документа не указан'}
        
        if not expiry_date:
            # Некоторые документы не имеют срока действия
            doc_info = self.DOCUMENT_REQUIREMENTS.get(doc_type, {})
            if doc_info.get('validity_days') is None:
                return {'valid': True, 'reason': 'Документ действует бессрочно'}
            else:
                return {'valid': False, 'reason': 'Срок действия не указан'}
        
        # Проверка даты истечения
        try:
            if isinstance(expiry_date, str):
                expiry = datetime.strptime(expiry_date, '%Y-%m-%d')
            else:
                expiry = expiry_date
            
            now = datetime.now()
            
            if expiry < now:
                return {
                    'valid': False,
                    'reason': f'Документ истёк {expiry.strftime("%Y-%m-%d")}',
                    'days_expired': (now - expiry).days
                }
            
            days_remaining = (expiry - now).days
            
            if days_remaining < 7:
                return {
                    'valid': True,
                    'warning': f'Документ истекает через {days_remaining} дней',
                    'days_remaining': days_remaining
                }
            
            return {
                'valid': True,
                'days_remaining': days_remaining
            }
            
        except Exception as e:
            return {'valid': False, 'reason': f'Ошибка проверки даты: {str(e)}'}
    
    def generate_document_checklist(
        self,
        order: Dict,
        safety_check: Optional[Dict] = None
    ) -> Dict:
        """
        Сгенерировать чеклист документов для заказа
        """
        cargo_type = order.get('cargo_type', 'general')
        is_international = self._is_international(order)
        
        required_docs = self.get_required_documents(cargo_type, is_international)
        
        # Добавить рекомендации
        recommendations = []
        
        if is_international and not any(d['type'] == 'origin_cert' for d in required_docs):
            recommendations.append(
                'Рекомендуем получить СТ-1 для освобождения от пошлин в СНГ'
            )
        
        if cargo_type == 'dangerous':
            recommendations.append(
                'Убедитесь что у водителя есть действующее свидетельство ДОПОГ'
            )
        
        return {
            'order_id': order.get('id'),
            'cargo_type': cargo_type,
            'is_international': is_international,
            'required_documents': required_docs,
            'recommendations': recommendations,
            'total_documents_required': len(required_docs)
        }
    
    def _is_international(self, order: Dict) -> bool:
        """Проверить является ли заказ международным"""
        pickup = order.get('pickup_address', '').lower()
        delivery = order.get('delivery_address', '').lower()
        
        # Упрощённая проверка - в реальности по координатам
        uzbek_cities = ['ташкент', 'самарканд', 'бухара', 'навои', 'фергана', 'андижан', 'намандан']
        
        pickup_in_uz = any(city in pickup for city in uzbek_cities)
        delivery_in_uz = any(city in delivery for city in uzbek_cities)
        
        return not (pickup_in_uz and delivery_in_uz)
