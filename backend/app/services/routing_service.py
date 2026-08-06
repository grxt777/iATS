"""
AI Route Validation Service
Построение и валидация маршрутов с учётом ограничений для грузов
Интеграция с Yandex Routing API, OpenWeatherMap, OpenRouteService
"""
import time
import requests
import numpy as np
from typing import Dict, List, Optional, Tuple
from loguru import logger
from app.core.config import get_settings

settings = get_settings()


class RouteValidationService:
    """
    AI-надстройка над Яндекс Routing API
    Проверяет маршрут на ограничения для конкретного груза
    """
    
    def __init__(self):
        self.yandex_api_key = settings.YANDEX_ROUTING_API_KEY
        self.weather_api_key = settings.OPENWEATHER_API_KEY
        self.ors_api_key = settings.OPENROUTESERVICE_API_KEY
        
        # Ограничения для ADR классов (из safety_service)
        self.adr_restrictions = {
            1: {'forbidden': ['tunnels', 'residential_zones']},
            3: {'forbidden': ['tunnels_class_c']},
            5: {'forbidden': ['tunnels', 'residential_zones']},
            7: {'forbidden': ['tunnels', 'residential_zones', 'schools']},
        }
    
    async def build_and_validate_route(
        self,
        order: Dict,
        vehicle: Dict,
        safety_check: Optional[Dict] = None,
        alternatives_count: int = 2
    ) -> Dict:
        """
        Построить маршрут и проверить его на ограничения
        """
        start_time = time.time()
        
        pickup = (order.get('pickup_lat'), order.get('pickup_lng'))
        delivery = (order.get('delivery_lat'), order.get('delivery_lng'))
        
        # Шаг 1: Получить базовый маршрут от Яндекса
        yandex_route = await self._get_yandex_route(pickup, delivery)
        
        if not yandex_route:
            return self._fallback_route(order, vehicle, pickup, delivery)
        
        # Шаг 2: Получить информацию об ограничениях дорог (OpenRouteService)
        road_restrictions = await self._get_road_restrictions(yandex_route['points'])
        
        # Шаг 3: Получить погоду на маршруте
        weather_data = await self._get_route_weather(yandex_route['points'])
        
        # Шаг 4: Проверить маршрут на ограничения для груза
        validation_result = self._validate_route_against_cargo(
            yandex_route,
            road_restrictions,
            weather_data,
            safety_check or {}
        )
        
        # Шаг 5: Если маршрут не подходит - найти альтернативу
        routes = [validation_result]
        
        if validation_result['validation_status'] != 'valid' and alternatives_count > 0:
            alternative = await self._find_alternative_route(
                pickup, delivery,
                validation_result.get('forbidden_segments', [])
            )
            if alternative:
                alternative['is_alternative'] = True
                alternative['alternative_rank'] = 2
                routes.append(alternative)
        
        # Шаг 6: Найти рекомендуемый маршрут
        recommended = self._select_best_route(routes)
        
        processing_time = (time.time() - start_time) * 1000
        
        return {
            'order_id': order.get('id'),
            'vehicle_id': vehicle.get('id'),
            'routes': routes,
            'recommended_route_id': recommended.get('route_id'),
            'processing_time_ms': round(processing_time, 2)
        }
    
    async def _get_yandex_route(self, start: Tuple[float, float], end: Tuple[float, float]) -> Optional[Dict]:
        """Получить маршрут от Yandex Routing API"""
        try:
            if not self.yandex_api_key:
                logger.warning("Yandex API key not set, using fallback")
                return None
            
            url = "https://api.routing.yandex.net/v2/route"
            params = {
                'start': f"{start[0]},{start[1]}",
                'end': f"{end[0]},{end[1]}",
                'mode': 'auto',
                'apikey': self.yandex_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Парсинг ответа Яндекса
            route = data.get('routes', [{}])[0]
            
            return {
                'total_distance_km': route.get('distance', 0) / 1000,
                'estimated_duration_min': route.get('duration', 0) / 60,
                'points': self._decode_polyline(route.get('geometry', '')),
                'segments': route.get('segments', [])
            }
            
        except Exception as e:
            logger.error(f"Yandex API error: {e}")
            return None
    
    async def _get_road_restrictions(self, route_points: List[Dict]) -> List[Dict]:
        """Получить ограничения дорог через OpenRouteService"""
        restrictions = []
        
        try:
            if not self.ors_api_key:
                return restrictions
            
            url = "https://api.openrouteservice.org/v2/directions/driving-hgv"
            
            # HGV профиль учитывает ограничения для грузовиков
            headers = {'Authorization': self.ors_api_key}
            
            coordinates = [[p['lng'], p['lat']] for p in route_points[::50]]  # Каждая 50-я точка
            
            data = {
                'coordinates': coordinates,
                'profile': 'driving-hgv',
                'preferences': {
                    'restrictions': {
                        'weight': 20,  # тонн
                        'height': 4,   # метра
                        'width': 2.55
                    }
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            # Извлечь предупреждения об ограничениях
            warnings = result.get('metadata', {}).get('warnings', [])
            for warning in warnings:
                restrictions.append({
                    'type': warning.get('code'),
                    'message': warning.get('message'),
                    'location': warning.get('location')
                })
            
        except Exception as e:
            logger.error(f"OpenRouteService error: {e}")
        
        return restrictions
    
    async def _get_route_weather(self, route_points: List[Dict]) -> List[Dict]:
        """Получить погоду вдоль маршрута"""
        weather_segments = []
        
        try:
            if not self.weather_api_key:
                return weather_segments
            
            # Проверяем погоду в ключевых точках маршрута
            sample_points = route_points[::len(route_points)//5] if len(route_points) > 5 else route_points
            
            for point in sample_points:
                url = "https://api.openweathermap.org/data/2.5/weather"
                params = {
                    'lat': point['lat'],
                    'lon': point['lng'],
                    'appid': self.weather_api_key,
                    'units': 'metric'
                }
                
                response = requests.get(url, params=params, timeout=5)
                response.raise_for_status()
                data = response.json()
                
                weather_segments.append({
                    'lat': point['lat'],
                    'lng': point['lng'],
                    'condition': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'temperature': data['main']['temp'],
                    'wind_speed': data.get('wind', {}).get('speed', 0),
                    'visibility': data.get('visibility', 10000),
                    'impact_score': self._calculate_weather_impact(data)
                })
            
        except Exception as e:
            logger.error(f"Weather API error: {e}")
        
        return weather_segments
    
    def _validate_route_against_cargo(
        self,
        route: Dict,
        road_restrictions: List[Dict],
        weather_data: List[Dict],
        safety_check: Dict
    ) -> Dict:
        """Проверить маршрут на соответствие ограничениям груза"""
        
        issues = []
        forbidden_segments = []
        
        adr_class = safety_check.get('adr_class')
        is_dangerous = safety_check.get('is_dangerous', False)
        is_perishable = safety_check.get('is_perishable', False)
        
        # Проверка тоннелей для опасных грузов
        if is_dangerous and adr_class:
            restrictions = self.adr_restrictions.get(adr_class, {})
            forbidden = restrictions.get('forbidden', [])
            
            if 'tunnels' in forbidden:
                # Отметить все тоннели как запрещённые
                for i, segment in enumerate(route.get('segments', [])):
                    if segment.get('has_tunnel'):
                        forbidden_segments.append({
                            'segment_index': i,
                            'reason': f'Тоннель запрещён для ADR класса {adr_class}'
                        })
                        issues.append(f"Сегмент {i}: тоннель запрещён для груза класса {adr_class}")
        
        # Проверка жилых зон
        if is_dangerous and 'residential_zones' in forbidden:
            for i, segment in enumerate(route.get('segments', [])):
                if segment.get('is_urban'):
                    forbidden_segments.append({
                        'segment_index': i,
                        'reason': 'Проезд через жилую зону запрещён для опасного груза'
                    })
        
        # Проверка погоды для скоропортящихся
        if is_perishable:
            for weather in weather_data:
                if weather.get('temperature', 20) > 30:
                    issues.append(f"Высокая температура ({weather['temperature']}°C) - риск порчи груза")
                elif weather.get('temperature', 20) < -10:
                    issues.append(f"Низкая температура ({weather['temperature']}°C) - риск замерзания")
        
        # Проверка ветра
        for weather in weather_data:
            if weather.get('wind_speed', 0) > 25:
                issues.append(f"Сильный ветер ({weather['wind_speed']} м/с) - опасно для высокого груза")
        
        # Определение статуса
        if len(forbidden_segments) > 0:
            validation_status = 'invalid'
        elif len(issues) > 0:
            validation_status = 'warning'
        else:
            validation_status = 'valid'
        
        # Расчёт стоимости
        distance_km = route.get('total_distance_km', 0)
        fuel_cost = distance_km * 12000  # 12000 UZS за км (примерно)
        
        return {
            'route_id': 1,
            'total_distance_km': distance_km,
            'estimated_duration_min': route.get('estimated_duration_min', 0),
            'estimated_fuel_cost_uzs': fuel_cost,
            'estimated_toll_cost_uzs': 0,
            'estimated_total_cost_uzs': fuel_cost,
            'validation_status': validation_status,
            'validation_issues': issues,
            'forbidden_segments': forbidden_segments,
            'segments': route.get('segments', []),
            'weather_data': weather_data,
            'road_restrictions': road_restrictions,
            'is_alternative': False,
            'alternative_rank': 1
        }
    
    async def _find_alternative_route(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        avoid_segments: List[Dict]
    ) -> Optional[Dict]:
        """Найти альтернативный маршрут, избегая запрещённых сегментов"""
        # В реальной реализации - запрос к Яндексу с avoid параметрами
        # Для MVP возвращаем None
        return None
    
    def _select_best_route(self, routes: List[Dict]) -> Dict:
        """Выбрать лучший маршрут из предложенных"""
        # Приоритет: valid > warning > invalid
        status_priority = {'valid': 0, 'warning': 1, 'invalid': 2}
        
        valid_routes = [r for r in routes if r.get('validation_status') == 'valid']
        if valid_routes:
            return min(valid_routes, key=lambda r: r.get('total_distance_km', 9999))
        
        warning_routes = [r for r in routes if r.get('validation_status') == 'warning']
        if warning_routes:
            return min(warning_routes, key=lambda r: r.get('total_distance_km', 9999))
        
        return routes[0] if routes else None
    
    def _fallback_route(self, order: Dict, vehicle: Dict, start: Tuple, end: Tuple) -> Dict:
        """Fallback маршрут если API недоступен"""
        from app.services.matching_service import SmartMatchingService
        
        distance_km = SmartMatchingService._haversine_distance(
            start[0], start[1], end[0], end[1]
        )
        
        return {
            'order_id': order.get('id'),
            'vehicle_id': vehicle.get('id'),
            'routes': [{
                'route_id': 1,
                'total_distance_km': round(distance_km, 2),
                'estimated_duration_min': round(distance_km / 60 * 60),
                'estimated_fuel_cost_uzs': round(distance_km * 12000, 2),
                'estimated_toll_cost_uzs': 0,
                'estimated_total_cost_uzs': round(distance_km * 12000, 2),
                'validation_status': 'warning',
                'validation_issues': ['API недоступен, маршрут рассчитан приблизительно'],
                'segments': [],
                'is_alternative': False,
                'alternative_rank': 1
            }],
            'recommended_route_id': 1,
            'processing_time_ms': 100
        }
    
    def _decode_polyline(self, polyline: str) -> List[Dict]:
        """Декодирование полилинии Яндекса в список точек"""
        # Упрощённая реализация
        points = []
        # В реальной реализации нужно декодировать Google polyline format
        return points
    
    def _calculate_weather_impact(self, weather_data: Dict) -> float:
        """Рассчитать влияние погоды на маршрут (0-1, выше=хуже)"""
        impact = 0.0
        
        condition = weather_data.get('weather', [{}])[0].get('main', '')
        temp = weather_data.get('main', {}).get('temp', 20)
        wind = weather_data.get('wind', {}).get('speed', 0)
        visibility = weather_data.get('visibility', 10000)
        
        if condition == 'Rain':
            impact += 0.2
        elif condition == 'Snow':
            impact += 0.4
        elif condition == 'Fog':
            impact += 0.3
        elif condition == 'Thunderstorm':
            impact += 0.5
        
        if temp > 35 or temp < -20:
            impact += 0.2
        
        if wind > 20:
            impact += 0.2
        
        if visibility < 1000:
            impact += 0.3
        
        return min(1.0, impact)
