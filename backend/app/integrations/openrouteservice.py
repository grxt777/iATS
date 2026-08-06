"""
OpenRouteService API Integration
Специализируется на маршрутах для грузовиков (HGV) с учётом ограничений
"""
import requests
from typing import Dict, List, Optional, Tuple
from loguru import logger
from app.core.config import get_settings

settings = get_settings()


class OpenRouteServiceIntegration:
    """
    Интеграция с OpenRouteService API
    Профиль driving-hgv учитывает ограничения для грузовиков
    """
    
    def __init__(self):
        self.api_key = settings.OPENROUTESERVICE_API_KEY
        self.base_url = "https://api.openrouteservice.org/v2"
    
    async def get_truck_route(
        self,
        coordinates: List[Tuple[float, float]],
        vehicle_specs: Optional[Dict] = None,
        avoid_features: Optional[List[str]] = None
    ) -> Optional[Dict]:
        """
        Построить маршрут для грузовика с учётом ограничений
        """
        try:
            if not self.api_key:
                logger.warning("OpenRouteService API key not set")
                return None
            
            headers = {
                'Authorization': self.api_key,
                'Content-Type': 'application/json'
            }
            
            # Преобразовать координаты в формат [lng, lat]
            coords = [[lng, lat] for lat, lng in coordinates]
            
            data = {
                'coordinates': coords,
                'profile': 'driving-hgv',
                'format': 'geojson',
                'preferences': {
                    'restrictions': {
                        'weight': vehicle_specs.get('weight_tons', 20) if vehicle_specs else 20,
                        'height': vehicle_specs.get('height_m', 4) if vehicle_specs else 4,
                        'width': vehicle_specs.get('width_m', 2.55) if vehicle_specs else 2.55,
                        'length': vehicle_specs.get('length_m', 12) if vehicle_specs else 12
                    }
                }
            }
            
            if avoid_features:
                data['preferences']['avoid_features'] = avoid_features
            
            response = requests.post(
                f"{self.base_url}/directions",
                json=data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            return self._parse_route_response(result)
            
        except Exception as e:
            logger.error(f"OpenRouteService error: {e}")
            return None
    
    async def get_road_restrictions(
        self,
        coordinates: List[Tuple[float, float]]
    ) -> List[Dict]:
        """
        Получить информацию об ограничениях на маршруте
        """
        try:
            if not self.api_key:
                return []
            
            headers = {'Authorization': self.api_key}
            
            coords = [[lng, lat] for lat, lng in coordinates]
            
            # Используем POI endpoint для поиска ограничений
            data = {
                'request': 'pois',
                'geometry': {
                    'bbox': self._get_bbox(coords),
                    'geojson': {
                        'type': 'LineString',
                        'coordinates': coords
                    }
                },
                'filters': {
                    'category_ids': [160, 170]  # Категории ограничений
                },
                'limit': 100
            }
            
            response = requests.post(
                f"{self.base_url}/pois",
                json=data,
                headers=headers,
                timeout=15
            )
            response.raise_for_status()
            result = response.json()
            
            restrictions = []
            for feature in result.get('features', []):
                props = feature.get('properties', {})
                restrictions.append({
                    'type': props.get('category_ids', []),
                    'name': props.get('name', ''),
                    'location': feature.get('geometry', {}).get('coordinates', [])
                })
            
            return restrictions
            
        except Exception as e:
            logger.error(f"Restrictions query error: {e}")
            return []
    
    async def check_tunnel_restrictions(
        self,
        route_points: List[Tuple[float, float]],
        adr_class: Optional[int] = None
    ) -> List[Dict]:
        """
        Проверить тоннели на маршруте на соответствие ADR ограничениям
        """
        try:
            if not self.api_key:
                return []
            
            headers = {'Authorization': self.api_key}
            
            coords = [[lng, lat] for lat, lng in route_points]
            
            # Поиск тоннелей
            data = {
                'request': 'pois',
                'geometry': {
                    'bbox': self._get_bbox(coords),
                    'geojson': {
                        'type': 'LineString',
                        'coordinates': coords
                    }
                },
                'filters': {
                    'category_ids': [570]  # Tunnel category
                },
                'limit': 50
            }
            
            response = requests.post(
                f"{self.base_url}/pois",
                json=data,
                headers=headers,
                timeout=15
            )
            response.raise_for_status()
            result = response.json()
            
            tunnels = []
            for feature in result.get('features', []):
                props = feature.get('properties', {})
                
                # Проверить ограничения для ADR класса
                restrictions = self._get_tunnel_adr_restrictions(
                    props.get('name', ''),
                    adr_class
                )
                
                tunnels.append({
                    'name': props.get('name', 'Unknown tunnel'),
                    'location': feature.get('geometry', {}).get('coordinates', []),
                    'adr_class': adr_class,
                    'is_forbidden': restrictions.get('forbidden', False),
                    'reason': restrictions.get('reason', ''),
                    'alternative_needed': restrictions.get('forbidden', False)
                })
            
            return tunnels
            
        except Exception as e:
            logger.error(f"Tunnel check error: {e}")
            return []
    
    def _get_tunnel_adr_restrictions(self, tunnel_name: str, adr_class: Optional[int]) -> Dict:
        """
        Получить ограничения тоннеля для ADR класса
        """
        # Категории тоннелей (A-E)
        # A - нет ограничений
        # B - запрещены взрывчатые (класс 1)
        # C - запрещены взрывчатые, газы, легковоспламеняющиеся (1, 2, 3)
        # D - запрещены 1, 2, 3, 4, 5
        # E - запрещены все опасные грузы
        
        if adr_class is None:
            return {'forbidden': False, 'reason': ''}
        
        # Упрощённая логика (в реальности нужно запрашивать данные тоннеля)
        tunnel_category = 'C'  # По умолчанию
        
        category_restrictions = {
            'A': [],
            'B': [1],
            'C': [1, 2, 3],
            'D': [1, 2, 3, 4, 5],
            'E': [1, 2, 3, 4, 5, 6, 7, 8, 9]
        }
        
        forbidden_classes = category_restrictions.get(tunnel_category, [])
        is_forbidden = adr_class in forbidden_classes
        
        return {
            'forbidden': is_forbidden,
            'reason': f"Тоннель категории {tunnel_category}, ADR класс {adr_class} {'запрещён' if is_forbidden else 'разрешён'}"
        }
    
    def _parse_route_response(self, response: Dict) -> Dict:
        """Разобрать ответ от OpenRouteService"""
        features = response.get('features', [])
        
        if not features:
            return None
        
        route = features[0]
        props = route.get('properties', {})
        segments = props.get('segments', [])
        
        # Извлечь информацию о сегментах
        segment_info = []
        for seg in segments:
            segment_info.append({
                'distance_km': seg.get('distance', 0) / 1000,
                'duration_min': seg.get('duration', 0) / 60,
                'steps': seg.get('steps', [])
            })
        
        return {
            'total_distance_km': props.get('summary', {}).get('distance', 0) / 1000,
            'total_duration_min': props.get('summary', {}).get('duration', 0) / 60,
            'geometry': route.get('geometry', {}).get('coordinates', []),
            'segments': segment_info,
            'bbox': response.get('bbox', []),
            'metadata': response.get('metadata', {})
        }
    
    def _get_bbox(self, coordinates: List[List[float]]) -> List[float]:
        """Получить bounding box для списка координат"""
        lats = [c[1] if len(c) > 1 else c[0] for c in coordinates]
        lngs = [c[0] if len(c) > 1 else c[1] for c in coordinates]
        
        return [
            min(lngs), min(lats),
            max(lngs), max(lats)
        ]
