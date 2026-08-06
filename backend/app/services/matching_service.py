"""
Smart Matching Service - AI подбор транспорта для груза
Использует XGBoost модель + эвристики
"""
import time
import numpy as np
from typing import List, Dict, Tuple, Optional
from sqlalchemy.orm import Session
from loguru import logger


class SmartMatchingService:
    """
    AI-powered matching engine для E-Logistika
    Оценивает совместимость груза и транспорта по 15+ признакам
    """
    
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Загрузка ML модели (если доступна)"""
        try:
            import joblib
            import os
            model_path = "app/ml/models/matching_model.pkl"
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info("ML matching model loaded successfully")
            else:
                logger.warning("ML model not found, using heuristic scoring")
        except Exception as e:
            logger.warning(f"Could not load ML model: {e}. Using heuristic scoring.")
    
    def extract_features(self, order: Dict, vehicle: Dict) -> Dict[str, float]:
        """Извлечение признаков для ML модели"""
        
        # Географические
        distance_to_pickup = self._haversine_distance(
            vehicle.get('current_lat', 0), vehicle.get('current_lng', 0),
            order.get('pickup_lat', 0), order.get('pickup_lng', 0)
        )
        distance_to_delivery = self._haversine_distance(
            order.get('pickup_lat', 0), order.get('pickup_lng', 0),
            order.get('delivery_lat', 0), order.get('delivery_lng', 0)
        )
        
        # Вместимость
        capacity_utilization = order.get('weight_kg', 0) / max(vehicle.get('capacity_kg', 1), 1)
        volume_utilization = order.get('volume_m3', 0) / max(vehicle.get('volume_m3', 1), 1) if vehicle.get('volume_m3') else 0
        
        # Финансовые
        estimated_cost = distance_to_delivery * vehicle.get('cost_per_km_uzs', 5000)
        budget_score = max(0, 1 - abs(estimated_cost - order.get('budget_uzs', 0)) / max(order.get('budget_uzs', 1), 1)) if order.get('budget_uzs') else 0.5
        
        # Технические
        cargo_type_match = 1.0 if order.get('cargo_type') == vehicle.get('compatible_cargo_type') else 0.7
        
        # Рейтинги
        driver_rating = vehicle.get('average_rating', 3.0) / 5.0
        success_rate = vehicle.get('success_rate', 0.8)
        
        # Допуски
        international_permit = 1.0 if vehicle.get('has_international_permit') else 0.0
        dangerous_goods_permit = 1.0 if vehicle.get('has_dangerous_goods_permit') else 0.0
        
        features = {
            'distance_to_pickup_km': distance_to_pickup,
            'distance_to_delivery_km': distance_to_delivery,
            'capacity_utilization': min(capacity_utilization, 1.5),
            'volume_utilization': min(volume_utilization, 1.5),
            'budget_score': budget_score,
            'cargo_type_match': cargo_type_match,
            'driver_rating': driver_rating,
            'success_rate': success_rate,
            'international_permit': international_permit,
            'dangerous_goods_permit': dangerous_goods_permit,
            'cost_per_km': vehicle.get('cost_per_km_uzs', 5000) / 10000,
            'total_trips': min(vehicle.get('total_trips', 0) / 100, 1.0),
            'profitability_coefficient': vehicle.get('profitability_coefficient', 1.0),
            'urgency_score': order.get('urgency_score', 5) / 10.0,
            'weight_fit': 1.0 if capacity_utilization <= 1.0 else 0.0
        }
        
        return features
    
    def calculate_heuristic_score(self, features: Dict[str, float]) -> Tuple[float, str]:
        """Эвристический scoring (если ML модель недоступна)"""
        
        # Веса для разных признаков
        weights = {
            'distance_to_pickup_km': -0.15,      # Чем ближе, тем лучше
            'capacity_utilization': 0.20,         # Оптимальная загрузка
            'budget_score': 0.15,                 # Соответствие бюджету
            'cargo_type_match': 0.15,             # Совместимость типа
            'driver_rating': 0.10,                # Рейтинг водителя
            'success_rate': 0.10,                 # Надёжность
            'international_permit': 0.05,         # Допуски
            'dangerous_goods_permit': 0.05,       # Допуски ОГ
            'weight_fit': 0.05,                   # Вместимость
        }
        
        score = 50.0  # Базовый score
        
        for feature, weight in weights.items():
            if feature in features:
                value = features[feature]
                if feature == 'distance_to_pickup_km':
                    # Нормализация расстояния (0-100 км = 1.0, >500 км = 0.0)
                    normalized = max(0, 1 - value / 500)
                    score += weight * normalized * 100
                else:
                    score += weight * value * 100
        
        score = max(0, min(100, score))
        
        # Определение confidence
        if score >= 80:
            confidence = "high"
        elif score >= 60:
            confidence = "medium"
        else:
            confidence = "low"
        
        return score, confidence
    
    def predict_match_score(self, features: Dict[str, float]) -> Tuple[float, str]:
        """Предсказание score совместимости"""
        
        if self.model is not None:
            # Использовать ML модель
            feature_vector = np.array(list(features.values())).reshape(1, -1)
            score = float(self.model.predict_proba(feature_vector)[0][1] * 100)
            confidence = "high" if score >= 80 else "medium" if score >= 60 else "low"
            return score, confidence
        else:
            # Использовать эвристики
            return self.calculate_heuristic_score(features)
    
    def find_best_matches(
        self, 
        db: Session,
        order: Dict,
        top_k: int = 5
    ) -> List[Dict]:
        """Найти лучшие совпадения для заказа"""
        
        start_time = time.time()
        
        # Получить все доступные транспорты
        from app.models.vehicle import Vehicle, VehicleStatus
        vehicles = db.query(Vehicle).filter(
            Vehicle.status == VehicleStatus.AVAILABLE
        ).all()
        
        results = []
        
        for vehicle in vehicles:
            # Извлечь признаки
            features = self.extract_features(order, {
                'current_lat': vehicle.current_lat,
                'current_lng': vehicle.current_lng,
                'capacity_kg': vehicle.capacity_kg,
                'volume_m3': vehicle.volume_m3,
                'cost_per_km_uzs': float(vehicle.cost_per_km_uzs or 5000),
                'average_rating': vehicle.average_rating,
                'success_rate': vehicle.success_rate,
                'total_trips': vehicle.total_trips,
                'has_international_permit': vehicle.has_international_permit,
                'has_dangerous_goods_permit': vehicle.has_dangerous_goods_permit,
                'profitability_coefficient': vehicle.profitability_coefficient,
                'compatible_cargo_type': None
            })
            
            # Рассчитать score
            score, confidence = self.predict_match_score(features)
            
            # Рассчитать расстояние и стоимость
            distance_km = features['distance_to_delivery_km']
            estimated_cost = distance_km * float(vehicle.cost_per_km_uzs or 5000)
            
            results.append({
                'vehicle_id': vehicle.id,
                'rank': 0,  # Будет установлено после сортировки
                'overall_score': round(score, 2),
                'confidence': confidence,
                'distance_score': round(features['distance_to_pickup_km'], 2),
                'capacity_score': round(features['capacity_utilization'] * 100, 2),
                'rating_score': round(features['driver_rating'] * 100, 2),
                'price_score': round(features['budget_score'] * 100, 2),
                'history_score': round(features['success_rate'] * 100, 2),
                'permit_score': round((features['international_permit'] + features['dangerous_goods_permit']) / 2 * 100, 2),
                'driver_name': None,  # Заполнить из БД
                'vehicle_type': vehicle.type.value,
                'license_plate': vehicle.license_plate,
                'current_distance_km': round(features['distance_to_pickup_km'], 2),
                'estimated_cost_uzs': round(estimated_cost, 2),
                'explanation': self._generate_explanation(features, score)
            })
        
        # Сортировка по score
        results.sort(key=lambda x: x['overall_score'], reverse=True)
        
        # Установка рангов
        for i, result in enumerate(results[:top_k]):
            result['rank'] = i + 1
        
        processing_time = (time.time() - start_time) * 1000
        
        return {
            'order_id': order.get('id'),
            'results': results[:top_k],
            'total_vehicles_evaluated': len(vehicles),
            'processing_time_ms': round(processing_time, 2)
        }
    
    def _generate_explanation(self, features: Dict, score: float) -> str:
        """Генерация объяснения почему этот транспорт подходит"""
        reasons = []
        
        if features['distance_to_pickup_km'] < 50:
            reasons.append(f"Близко к грузу ({features['distance_to_pickup_km']:.0f} км)")
        
        if features['capacity_utilization'] > 0.7:
            reasons.append(f"Хорошая загрузка ({features['capacity_utilization']*100:.0f}%)")
        
        if features['driver_rating'] > 0.8:
            reasons.append(f"Высокий рейтинг водителя ({features['driver_rating']*5:.1f}/5)")
        
        if features['success_rate'] > 0.9:
            reasons.append(f"Надёжный перевозчик ({features['success_rate']*100:.0f}% успешных рейсов)")
        
        if features['international_permit'] > 0:
            reasons.append("Есть международные допуски")
        
        if not reasons:
            reasons.append("Стандартное совпадение")
        
        return "; ".join(reasons)
    
    @staticmethod
    def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Расчет расстояния между двумя точками (в км)"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371  # Радиус Земли в км
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
