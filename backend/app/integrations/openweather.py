"""
OpenWeatherMap API Integration
"""
import requests
from typing import Dict, List, Optional, Tuple
from loguru import logger
from app.core.config import get_settings

settings = get_settings()


class OpenWeatherIntegration:
    """
    Интеграция с OpenWeatherMap API
    """
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    async def get_current_weather(self, lat: float, lng: float) -> Optional[Dict]:
        """
        Получить текущую погоду по координатам
        """
        try:
            if not self.api_key:
                logger.warning("OpenWeather API key not set")
                return None
            
            params = {
                'lat': lat,
                'lon': lng,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'ru'
            }
            
            response = requests.get(f"{self.base_url}/weather", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'location': {
                    'name': data.get('name', ''),
                    'country': data.get('sys', {}).get('country', ''),
                    'lat': data.get('coord', {}).get('lat', lat),
                    'lng': data.get('coord', {}).get('lon', lng)
                },
                'weather': {
                    'main': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                },
                'temperature': {
                    'current': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'min': data['main']['temp_min'],
                    'max': data['main']['temp_max']
                },
                'wind': {
                    'speed': data.get('wind', {}).get('speed', 0),
                    'direction': data.get('wind', {}).get('deg', 0)
                },
                'visibility': data.get('visibility', 10000),
                'humidity': data['main'].get('humidity', 0),
                'pressure': data['main'].get('pressure', 0),
                'impact_score': self._calculate_impact_score(data),
                'recommendations': self._generate_recommendations(data)
            }
            
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            return None
    
    async def get_forecast(self, lat: float, lng: float, days: int = 5) -> Optional[List[Dict]]:
        """
        Получить прогноз погоды на N дней
        """
        try:
            if not self.api_key:
                return None
            
            params = {
                'lat': lat,
                'lon': lng,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'ru',
                'cnt': days * 8  # Прогноз каждые 3 часа
            }
            
            response = requests.get(f"{self.base_url}/forecast", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            forecast = []
            for item in data.get('list', []):
                forecast.append({
                    'datetime': item.get('dt_txt'),
                    'temperature': item['main']['temp'],
                    'weather': item['weather'][0]['main'],
                    'description': item['weather'][0]['description'],
                    'wind_speed': item.get('wind', {}).get('speed', 0),
                    'impact_score': self._calculate_impact_score(item)
                })
            
            return forecast
            
        except Exception as e:
            logger.error(f"Forecast API error: {e}")
            return None
    
    async def get_route_weather(self, route_points: List[Tuple[float, float]]) -> List[Dict]:
        """
        Получить погоду вдоль маршрута
        """
        weather_segments = []
        
        # Проверяем погоду в ключевых точках маршрута
        sample_points = self._sample_route_points(route_points, max_points=10)
        
        for lat, lng in sample_points:
            weather = await self.get_current_weather(lat, lng)
            if weather:
                weather_segments.append(weather)
        
        return weather_segments
    
    def _calculate_impact_score(self, weather_data: Dict) -> float:
        """
        Рассчитать влияние погоды на перевозку (0-1, выше=хуже)
        """
        score = 0.0
        
        condition = weather_data.get('weather', [{}])[0].get('main', '')
        temp = weather_data.get('main', {}).get('temp', 20)
        wind = weather_data.get('wind', {}).get('speed', 0)
        visibility = weather_data.get('visibility', 10000)
        
        # Осадки
        if condition == 'Rain':
            score += 0.2
        elif condition == 'Snow':
            score += 0.4
        elif condition == 'Fog':
            score += 0.3
        elif condition == 'Thunderstorm':
            score += 0.5
        elif condition == 'Hail':
            score += 0.6
        
        # Температура
        if temp > 35:
            score += 0.3  # Жара - риск для скоропортящихся
        elif temp > 30:
            score += 0.15
        elif temp < -20:
            score += 0.4  # Сильный мороз
        elif temp < -10:
            score += 0.2
        
        # Ветер
        if wind > 25:
            score += 0.3  # Опасно для высокого груза
        elif wind > 15:
            score += 0.15
        
        # Видимость
        if visibility < 500:
            score += 0.5
        elif visibility < 1000:
            score += 0.3
        elif visibility < 5000:
            score += 0.1
        
        return min(1.0, score)
    
    def _generate_recommendations(self, weather_data: Dict) -> List[str]:
        """
        Сгенерировать рекомендации для водителя
        """
        recommendations = []
        
        condition = weather_data.get('weather', [{}])[0].get('main', '')
        temp = weather_data.get('main', {}).get('temp', 20)
        wind = weather_data.get('wind', {}).get('speed', 0)
        
        if condition == 'Rain':
            recommendations.append("Дождь - увеличьте дистанцию, снизьте скорость")
        elif condition == 'Snow':
            recommendations.append("Снегопад - используйте зимнюю резину, снизьте скорость")
        elif condition == 'Fog':
            recommendations.append("Туман - включите противотуманные фары, снизьте скорость")
        elif condition == 'Thunderstorm':
            recommendations.append("Гроза - рекомендуется остановиться и переждать")
        
        if temp > 35:
            recommendations.append("Жара - проверьте кондиционер, берите больше воды")
        elif temp < -20:
            recommendations.append("Сильный мороз - проверьте антифриз, утеплите груз")
        
        if wind > 20:
            recommendations.append("Сильный ветер - осторожно на мостах и открытых участках")
        
        return recommendations
    
    def _sample_route_points(self, points: List[Tuple[float, float]], max_points: int = 10) -> List[Tuple[float, float]]:
        """Выбрать ключевые точки маршрута для проверки погоды"""
        if len(points) <= max_points:
            return points
        
        step = len(points) // max_points
        return points[::step]
