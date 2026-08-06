"""
Cargo Safety Check Service - AI проверка безопасности груза
Определяет тип груза, класс опасности ADR, необходимые документы
"""
import time
import re
from typing import Dict, List, Optional, Tuple
from loguru import logger


# База данных типов грузов и их требований
CARGO_DATABASE = {
    # Скоропортящиеся (фрукты, овощи)
    'яблоки': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    'груши': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    'виноград': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    'помидоры': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    'огурцы': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    'картофель': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    'морковь': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    'бананы': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    'апельсины': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    'клубника': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    
    # Зерновые
    'пшеница': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    'кукуруза': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    'хлопок': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    'рис': {'type': 'perishable', 'adr_class': None, 'needs_phytosanitary': True},
    
    # Опасные грузы (ADR)
    'аммиачная селитра': {'type': 'dangerous', 'adr_class': 5, 'un_number': 'UN1942', 'name': 'Окисляющие вещества'},
    'бензин': {'type': 'dangerous', 'adr_class': 3, 'un_number': 'UN1203', 'name': 'Легковоспламеняющиеся жидкости'},
    'дизельное топливо': {'type': 'dangerous', 'adr_class': 3, 'un_number': 'UN1202', 'name': 'Легковоспламеняющиеся жидкости'},
    'природный газ': {'type': 'dangerous', 'adr_class': 2, 'un_number': 'UN1971', 'name': 'Газы'},
    'серная кислота': {'type': 'dangerous', 'adr_class': 8, 'un_number': 'UN1830', 'name': 'Коррозионные вещества'},
    'хлор': {'type': 'dangerous', 'adr_class': 2, 'un_number': 'UN1017', 'name': 'Газы (токсичные)'},
    'цианид': {'type': 'dangerous', 'adr_class': 6, 'un_number': 'UN1689', 'name': 'Токсичные вещества'},
    'тротил': {'type': 'dangerous', 'adr_class': 1, 'un_number': 'UN0209', 'name': 'Взрывчатые вещества'},
    'радиоактивные материалы': {'type': 'dangerous', 'adr_class': 7, 'un_number': 'UN2912', 'name': 'Радиоактивные материалы'},
    'литиевые батареи': {'type': 'dangerous', 'adr_class': 9, 'un_number': 'UN3480', 'name': 'Прочие опасные'},
    
    # Обычные грузы
    'электроника': {'type': 'general', 'adr_class': None},
    'одежда': {'type': 'general', 'adr_class': None},
    'мебель': {'type': 'general', 'adr_class': None},
    'строительные материалы': {'type': 'general', 'adr_class': None},
    'цемент': {'type': 'general', 'adr_class': None},
    'кирпич': {'type': 'general', 'adr_class': None},
    'металл': {'type': 'general', 'adr_class': None},
    'сталь': {'type': 'general', 'adr_class': None},
    'пластик': {'type': 'general', 'adr_class': None},
    'стекло': {'type': 'general', 'adr_class': None},
}

# Маршрутные ограничения для разных классов ADR
ADR_ROUTE_RESTRICTIONS = {
    1: {  # Взрывчатые
        'forbidden': ['tunnels', 'residential_zones', 'urban_centers'],
        'min_distance_urban': 5000,  # метров
        'special_requirements': ['armed_escort', 'special_marking', 'night_restrictions']
    },
    2: {  # Газы
        'forbidden': ['tunnels_without_ventilation', 'ferries_without_gas_permit'],
        'special_requirements': ['ventilation_required', 'temperature_monitoring']
    },
    3: {  # Легковоспламеняющиеся жидкости
        'forbidden': ['tunnels_class_c', 'water_protected_zones'],
        'special_requirements': ['fire_extinguisher', 'grounding_required', 'no_smoking_500m']
    },
    5: {  # Окисляющие вещества (аммиачная селитра)
        'forbidden': ['tunnels', 'residential_zones', 'near_food_storage'],
        'min_distance_urban': 2000,
        'special_requirements': ['no_contact_with_organics', 'temperature_below_30C', 'moisture_protection']
    },
    6: {  # Токсичные
        'forbidden': ['tunnels', 'water_sources_proximity', 'food_transport_routes'],
        'special_requirements': ['hazmat_suit', 'emergency_decon_kit', 'special_routing']
    },
    7: {  # Радиоактивные
        'forbidden': ['tunnels', 'residential_zones', 'schools', 'hospitals', 'water_sources'],
        'min_distance_urban': 10000,
        'special_requirements': ['radiation_monitoring', 'lead_shielding', 'escort_vehicle', 'pre_notification']
    },
    8: {  # Коррозионные
        'forbidden': ['water_bridges', 'environmental_zones'],
        'special_requirements': ['spill_kit', 'neutralizing_agent', 'corrosion_resistant_container']
    },
}


class SafetyCheckService:
    """
    AI-powered проверка безопасности груза
    """
    
    def __init__(self):
        self.cargo_db = CARGO_DATABASE
        self.adr_restrictions = ADR_ROUTE_RESTRICTIONS
    
    def classify_cargo(self, cargo_name: str, cargo_description: Optional[str] = None) -> Dict:
        """
        Классификация груза по названию/описанию
        Возвращает тип груза, ADR класс, необходимые документы
        """
        cargo_lower = cargo_name.lower().strip()
        
        # Прямое совпадение
        if cargo_lower in self.cargo_db:
            return self.cargo_db[cargo_lower]
        
        # Нечёткий поиск
        for key, value in self.cargo_db.items():
            if key in cargo_lower or cargo_lower in key:
                return value
        
        # Если не нашли - считаем обычным грузом
        return {
            'type': 'general',
            'adr_class': None,
            'needs_phytosanitary': False
        }
    
    def get_required_documents(self, cargo_info: Dict, is_international: bool = False) -> List[str]:
        """Определить список необходимых документов для груза"""
        docs = [
            'ettn',           # Электронная ТТН
            'waybill',        # Путевой лист
            'license',        # Лицензия перевозчика
        ]
        
        cargo_type = cargo_info.get('type')
        
        # Для скоропортящихся
        if cargo_type == 'perishable' or cargo_info.get('needs_phytosanitary'):
            docs.append('phytosanitary')
            docs.append('sanitary')
        
        # Для опасных грузов
        if cargo_type == 'dangerous':
            docs.append('adr_cert')
            docs.append('dg_permit')
            docs.append('emergency_card')
            docs.append('insurance')
        
        # Для международных
        if is_international:
            docs.append('cmr')
            docs.append('customs_decl')
            docs.append('origin_cert')  # СТ-1
        
        return docs
    
    def get_route_restrictions(self, adr_class: Optional[int]) -> Dict:
        """Получить ограничения маршрута для класса опасности"""
        if adr_class is None or adr_class not in self.adr_restrictions:
            return {
                'forbidden': [],
                'special_requirements': []
            }
        
        return self.adr_restrictions.get(adr_class, {
            'forbidden': [],
            'special_requirements': []
        })
    
    def calculate_risk_score(self, cargo_info: Dict, order: Dict) -> Tuple[int, str, List[str]]:
        """
        Рассчитать риск-скор груза (0-100)
        Возвращает: score, risk_level, risk_factors
        """
        score = 0
        risk_factors = []
        
        # Базовый риск по типу
        cargo_type = cargo_info.get('type', 'general')
        
        if cargo_type == 'general':
            score = 10
        elif cargo_type == 'perishable':
            score = 30
            risk_factors.append("Скоропортящийся груз - риск порчи")
        elif cargo_type == 'dangerous':
            adr_class = cargo_info.get('adr_class', 9)
            # Разные классы имеют разный риск
            base_scores = {1: 95, 2: 75, 3: 70, 5: 70, 6: 85, 7: 95, 8: 65, 9: 50}
            score = base_scores.get(adr_class, 50)
            risk_factors.append(f"Опасный груз ADR класс {adr_class}")
            
            if cargo_info.get('un_number'):
                risk_factors.append(f"UN номер: {cargo_info['un_number']}")
        elif cargo_type == 'oversized':
            score = 40
            risk_factors.append("Крупногабаритный груз - ограничения маршрута")
        elif cargo_type == 'valuable':
            score = 45
            risk_factors.append("Ценный груз - риск кражи")
        
        # Дополнительные факторы
        if order.get('urgency_score', 5) >= 8:
            score += 5
            risk_factors.append("Высокая срочность - меньше времени на проверки")
        
        if order.get('weight_kg', 0) > 20000:
            score += 5
            risk_factors.append("Большой вес - ограничения по мостам")
        
        # Нормализация
        score = max(0, min(100, score))
        
        # Определение уровня риска
        if score >= 80:
            risk_level = 'critical'
        elif score >= 60:
            risk_level = 'high'
        elif score >= 30:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return score, risk_level, risk_factors
    
    def check_order_safety(
        self, 
        order: Dict,
        documents_provided: Optional[List[str]] = None
    ) -> Dict:
        """
        Полная проверка безопасности заказа
        """
        start_time = time.time()
        
        # Классификация груза
        cargo_info = self.classify_cargo(
            order.get('cargo_name', ''),
            order.get('cargo_description')
        )
        
        # Определение необходимых документов
        is_international = self._is_international_order(order)
        required_docs = self.get_required_documents(cargo_info, is_international)
        
        # Проверка предоставленных документов
        docs_provided = documents_provided or []
        docs_missing = [doc for doc in required_docs if doc not in docs_provided]
        docs_valid = {doc: doc in docs_provided for doc in required_docs}
        
        # Расчёт риска
        risk_score, risk_level, risk_factors = self.calculate_risk_score(cargo_info, order)
        
        # Ограничения маршрута
        route_restrictions = self.get_route_restrictions(cargo_info.get('adr_class'))
        
        # Определение статуса
        if docs_missing and cargo_info.get('type') == 'dangerous':
            status = 'failed'
        elif docs_missing and cargo_info.get('type') == 'perishable':
            status = 'needs_review'
        elif risk_level in ['critical', 'high']:
            status = 'needs_review'
        else:
            status = 'passed'
        
        processing_time = (time.time() - start_time) * 1000
        
        return {
            'order_id': order.get('id'),
            'cargo_name': order.get('cargo_name', ''),
            'detected_cargo_type': cargo_info.get('type', 'general'),
            
            'is_perishable': cargo_info.get('type') == 'perishable' or cargo_info.get('needs_phytosanitary', False),
            'is_dangerous': cargo_info.get('type') == 'dangerous',
            'adr_class': cargo_info.get('adr_class'),
            'adr_class_name': cargo_info.get('name'),
            'un_number': cargo_info.get('un_number'),
            
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            
            'required_documents': required_docs,
            'documents_provided': docs_provided,
            'documents_missing': docs_missing,
            'documents_valid': docs_valid,
            
            'route_restrictions': route_restrictions.get('forbidden', []),
            'forbidden_segments': [],  # Заполняется при проверке маршрута
            'special_requirements': route_restrictions.get('special_requirements', []),
            
            'ai_confidence': 0.85,  # Confidence of classification
            'status': status,
            'processing_time_ms': round(processing_time, 2),
            'notes': f"Груз классифицирован как {cargo_info.get('type', 'general')}"
        }
    
    def verify_document(self, document_data: Dict) -> Dict:
        """
        AI проверка документа (NLP извлечение данных)
        """
        # Симуляция NLP анализа
        extracted_fields = {}
        confidence = 0.0
        warnings = []
        
        doc_type = document_data.get('type')
        
        if doc_type == 'phytosanitary':
            # Извлечение данных из фитосанитарного сертификата
            extracted_fields = {
                'cargo_name': document_data.get('cargo_name'),
                'weight_kg': document_data.get('weight'),
                'origin_country': document_data.get('origin'),
                'destination_country': document_data.get('destination'),
                'vehicle_number': document_data.get('vehicle_number'),
                'issue_date': document_data.get('issue_date'),
                'expiry_date': document_data.get('expiry_date')
            }
            confidence = 0.92
            
            # Проверка срока действия
            if document_data.get('expiry_date'):
                from datetime import datetime
                try:
                    expiry = datetime.strptime(document_data['expiry_date'], '%Y-%m-%d')
                    if expiry < datetime.now():
                        warnings.append("Срок действия сертификата истёк")
                    elif (expiry - datetime.now()).days < 7:
                        warnings.append("Срок действия сертификата истекает менее чем через 7 дней")
                except:
                    warnings.append("Не удалось проверить срок действия")
        
        elif doc_type == 'adr_cert':
            extracted_fields = {
                'driver_name': document_data.get('driver_name'),
                'adr_classes': document_data.get('classes', []),
                'issue_date': document_data.get('issue_date'),
                'expiry_date': document_data.get('expiry_date')
            }
            confidence = 0.88
        
        return {
            'document_id': document_data.get('id'),
            'is_valid': len(warnings) == 0,
            'extracted_data': extracted_fields,
            'confidence': confidence,
            'warnings': warnings,
            'expiry_date': extracted_fields.get('expiry_date'),
            'is_expired': any('истёк' in w for w in warnings)
        }
    
    def _is_international_order(self, order: Dict) -> bool:
        """Проверить является ли заказ международным"""
        # Упрощённая логика - в реальности нужно проверять координаты
        pickup = order.get('pickup_address', '').lower()
        delivery = order.get('delivery_address', '').lower()
        
        uzbek_cities = ['ташкент', 'самарканд', 'бухара', 'навои', 'фергана', 'андижан']
        
        pickup_in_uz = any(city in pickup for city in uzbek_cities)
        delivery_in_uz = any(city in delivery for city in uzbek_cities)
        
        return not (pickup_in_uz and delivery_in_uz)
