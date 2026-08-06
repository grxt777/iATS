"""
Yandex Maps & Routing API Integration
"""
import requests
from typing import Dict, List, Optional, Tuple
from loguru import logger
from app.core.config import get_settings

settings = get_settings()


class YandexMapsIntegration:
    """
    Интеграция с Yandex Maps API
    """
    
    def __init__(self):
        self.api_key = settings.YANDEX_MAPS_API_KEY
        self.routing_api_key = settings.YANDEX_ROUTING_API_KEY
        self.base_url = "https://geocode-maps.yandex.ru/1.x/"
        self.routing_url = "https://api.routing.yandex.net/v2/route"
    
    async def geocode(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Геокодирование: адрес -> координаты
        """
        try:
            if not self.api_key:
                logger.warning("Yandex Maps API key not set")
                return None
            
            params = {
                'geocode': address,
                'format': 'json',
                'apikey': self.api_key,
                'results': 1
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            pos = (data['response']
                    ['GeoObjectCollection']
                    ['featureMember'][0]
                    ['GeoObject']
                    ['Point']
                    ['pos'])
            
            # Yandex возвращает "lng lat"
            lng, lat = map(float, pos.split(' '))
            return (lat, lng)
            
        except Exception as e:
            logger.error(f"Geocoding error: {e}")
            return None
    
    async def reverse_geocode(self, lat: float, lng: float) -> Optional[str]:
        """
        Обратное геокодирование: координаты -> адрес
        """
        try:
            if not self.api_key:
                return None
            
            params = {
                'geocode': f"{lng},{lat}",
                'format': 'json',
                'apikey': self.api_key,
                'results': 1
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            address = (data['response']
                       ['GeoObjectCollection']
                       ['featureMember'][0]
                       ['GeoObject']
                       ['metaDataProperty']
                       ['GeocoderMetaData']
                       ['text'])
            
            return address
            
        except Exception as e:
            logger.error(f"Reverse geocoding error: {e}")
            return None
    
    async def get_route(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        vehicle_type: str = 'auto'
    ) -> Optional[Dict]:
        """
        Построить маршрут между двумя точками
        """
        try:
            if not self.routing_api_key:
                logger.warning("Yandex Routing API key not set")
                return None
            
            params = {
                'start': f"{start[0]},{start[1]}",
                'end': f"{end[0]},{end[1]}",
                'mode': vehicle_type,
                'apikey': self.routing_api_key
            }
            
            response = requests.get(self.routing_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'routes' not in data or not data['routes']:
                return None
            
            route = data['routes'][0]
            
            return {
                'distance_km': route.get('distance', 0) / 1000,
                'duration_min': route.get('duration', 0) / 60,
                'geometry': route.get('geometry', ''),
                'segments': route.get('segments', [])
            }
            
        except Exception as e:
            logger.error(f"Routing error: {e}")
            return None
    
    async def search_nearby(
        self,
        lat: float,
        lng: float,
        query: str,
        radius: int = 5000
    ) -> List[Dict]:
        """
        Поиск объектов поблизости (АЗС, мотели, пункты взвешивания)
        """
        try:
            if not self.api_key:
                return []
            
            url = "https://search-maps.yandex.ru/v1/"
            params = {
                'text': query,
                'll': f"{lng},{lat}",
                'spn': f"{radius/111000},{radius/111000}",
                'format': 'json',
                'apikey': self.api_key,
                'results': 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for feature in data.get('features', []):
                props = feature.get('properties', {})
                geom = feature.get('geometry', {})
                
                results.append({
                    'name': props.get('name', ''),
                    'description': props.get('description', ''),
                    'address': props.get('address', {}).get('formatted', ''),
                    'lat': geom.get('coordinates', [0, 0])[1],
                    'lng': geom.get('coordinates', [0, 0])[0]
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
