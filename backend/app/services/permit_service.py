"""
Permit Management Service
Управление рухсатнома (разрешениями на международные перевозки)
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from loguru import logger


class PermitService:
    """
    Сервис управления разрешениями на международные перевозки
    Мониторинг квот, прогнозирование дефицита
    """
    
    # Страны с которыми у Узбекистана есть соглашения
    PARTNER_COUNTRIES = {
        'RU': 'Россия',
        'KZ': 'Казахстан',
        'KG': 'Кыргызстан',
        'TJ': 'Таджикистан',
        'TM': 'Туркменистан',
        'CN': 'Китай',
        'TR': 'Турция',
        'IR': 'Иран',
        'AF': 'Афганистан',
        'BY': 'Беларусь',
    }
    
    # История дефицитов по направлениям (для ML прогнозирования)
    DEFICIT_HISTORY = {
        'RU': {'months_with_deficit': [6, 7, 8, 12], 'avg_deficit_percent': 35},
        'CN': {'months_with_deficit': [3, 4, 9, 10], 'avg_deficit_percent': 45},
        'KZ': {'months_with_deficit': [5, 6, 7], 'avg_deficit_percent': 20},
        'TR': {'months_with_deficit': [4, 5, 11], 'avg_deficit_percent': 30},
    }
    
    def predict_permit_availability(
        self,
        country_code: str,
        permit_type: str,
        months_ahead: int = 3
    ) -> List[Dict]:
        """
        Прогноз доступности разрешений на N месяцев вперёд
        Использует исторические данные для прогнозирования дефицита
        """
        predictions = []
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        country_deficit = self.DEFICIT_HISTORY.get(country_code, {
            'months_with_deficit': [],
            'avg_deficit_percent': 10
        })
        
        for i in range(months_ahead):
            month = (current_month + i) % 12 or 12
            year = current_year + ((current_month + i) // 12)
            
            # Вероятность дефицита
            if month in country_deficit['months_with_deficit']:
                deficit_probability = 0.7 + (country_deficit['avg_deficit_percent'] / 200)
                recommendation = 'high'
            else:
                deficit_probability = 0.2
                recommendation = 'low'
            
            predictions.append({
                'year': year,
                'month': month,
                'month_name': datetime(year, month, 1).strftime('%B'),
                'deficit_probability': round(deficit_probability, 2),
                'recommendation': recommendation,
                'action': self._get_recommendation_action(recommendation)
            })
        
        return predictions
    
    def check_carrier_eligibility(
        self,
        profitability_coefficient: float,
        permit_type: str,
        country_quota: int
    ) -> Dict:
        """
        Проверить имеет ли перевозчик право на получение разрешения
        согласно новым правилам с 1 июня 2026
        """
        
        # Правила для квот <= 1000
        if country_quota <= 1000:
            if profitability_coefficient >= 1.0:
                return {
                    'eligible': True,
                    'reason': f'Коэффициент доходности {profitability_coefficient} >= 1.0',
                    'restrictions': ['Только маршрут с загрузкой в обе стороны']
                }
            else:
                return {
                    'eligible': False,
                    'reason': f'Коэффициент доходности {profitability_coefficient} < 1.0',
                    'alternatives': ['Повысьте коэффициент доходности до 1.0+']
                }
        
        # Правила для квот > 1000
        else:
            if profitability_coefficient >= 0.7:
                return {
                    'eligible': True,
                    'reason': f'Коэффициент доходности {profitability_coefficient} >= 0.7',
                    'restrictions': []
                }
            else:
                return {
                    'eligible': False,
                    'reason': f'Коэффициент доходности {profitability_coefficient} < 0.7',
                    'alternatives': ['Повысьте коэффициент доходности до 0.7+']
                }
    
    def calculate_permit_cost(
        self,
        permit_type: str,
        country_code: str
    ) -> Dict:
        """
        Рассчитать стоимость получения разрешения
        """
        # Базовая стоимость: 1/4 БРВ
        base_fee = 82500  # UZS
        
        # Дополнительные сборы в зависимости от типа
        type_multipliers = {
            'bilateral': 1.0,
            'transit': 1.5,
            'third_country': 2.0
        }
        
        fee = base_fee * type_multipliers.get(permit_type, 1.0)
        
        return {
            'base_fee_uzs': base_fee,
            'type_multiplier': type_multipliers.get(permit_type, 1.0),
            'total_fee_uzs': fee,
            'currency': 'UZS',
            'validity_days': 90,
            'return_deadline_days': 90
        }
    
    def get_permit_status_summary(self) -> Dict:
        """
        Получить сводку по статусу разрешений
        """
        summary = {
            'total_countries': len(self.PARTNER_COUNTRIES),
            'countries_with_deficit': 0,
            'recommendations': []
        }
        
        for country_code, country_name in self.PARTNER_COUNTRIES.items():
            current_month = datetime.now().month
            
            country_deficit = self.DEFICIT_HISTORY.get(country_code, {})
            months_with_deficit = country_deficit.get('months_with_deficit', [])
            
            if current_month in months_with_deficit:
                summary['countries_with_deficit'] += 1
                summary['recommendations'].append({
                    'country': country_name,
                    'country_code': country_code,
                    'status': 'deficit',
                    'action': f'Срочно подать заявку - дефицит разрешений в {datetime.now().strftime("%B")}'
                })
            else:
                summary['recommendations'].append({
                    'country': country_name,
                    'country_code': country_code,
                    'status': 'available',
                    'action': 'Разрешения доступны'
                })
        
        return summary
    
    def _get_recommendation_action(self, recommendation: str) -> str:
        """Получить рекомендацию к действию"""
        actions = {
            'high': 'Срочно подать заявку - высокий риск дефицита',
            'medium': 'Рекомендуем подать заявку в ближайшее время',
            'low': 'Разрешения доступны, можно подать позже'
        }
        return actions.get(recommendation, '')
