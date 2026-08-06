# 🚀 QUICK START GUIDE
## Запуск AI Logistics Platform за 5 минут

---

##  ПРЕДВАРИТЕЛЬНЫЕ ТРЕБОВАНИЯ

- Docker & Docker Compose
- Python 3.11+ (для локального запуска)
- Node.js 18+ (для локального запуска)
- API ключи:
  - Yandex Maps & Routing API
  - OpenWeatherMap API
  - OpenRouteService API

---

##  ВАРИАНТ 1: DOCKER (РЕКОМЕНДУЕТСЯ)

### Шаг 1: Клонируйте проект
```bash
cd /home/user/ai-logistics-platform
```

### Шаг 2: Создайте .env файл
```bash
cp backend/.env.example backend/.env
```

Отредактируйте `backend/.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/logistics
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-super-secret-key

# API Keys (получить бесплатно)
YANDEX_MAPS_API_KEY=your-yandex-key
YANDEX_ROUTING_API_KEY=your-yandex-routing-key
OPENWEATHER_API_KEY=your-weather-key
OPENROUTESERVICE_API_KEY=your-ors-key
```

### Шаг 3: Запустите все сервисы
```bash
docker-compose up -d
```

### Шаг 4: Проверьте статус
```bash
docker-compose ps
```

Должны быть запущены:
- ✅ logistics-postgres
- ✅ logistics-redis
- ✅ logistics-backend
- ✅ logistics-frontend
- ✅ logistics-telegram-miniapp
- ✅ logistics-nginx

### Шаг 5: Откройте в браузере
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Telegram Mini App:** http://localhost:3001

---

##  ВАРИАНТ 2: ЛОКАЛЬНЫЙ ЗАПУСК (для разработки)

### Backend

```bash
cd backend

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Создать .env файл
cp .env.example .env
# Отредактировать .env

# Запустить PostgreSQL и Redis (через Docker)
docker-compose up -d postgres redis

# Запустить backend
uvicorn app.main:app --reload
```

Backend запустится на http://localhost:8000

### Frontend

```bash
cd frontend

# Установить зависимости
npm install

# Создать .env файл
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Запустить
npm start
```

Frontend запустится на http://localhost:3000

### Telegram Mini App

```bash
cd telegram-miniapp

# Установить зависимости
npm install

# Создать .env файл
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Запустить
npm start
```

Telegram Mini App запустится на http://localhost:3001

---

##  ПОЛУЧЕНИЕ API КЛЮЧЕЙ

### Yandex Maps & Routing API
1. Перейти: https://developer.tech.yandex.ru/
2. Зарегистрироваться
3. Создать новый проект
4. Получить API ключ
5. **Важно:** Указать что вы участник хакатона (могут дать повышенные лимиты)

### OpenWeatherMap API
1. Перейти: https://openweathermap.org/api
2. Зарегистрироваться (бесплатно)
3. Перейти в раздел "My API Keys"
4. Скопировать ключ
5. Бесплатный лимит: 1,000,000 запросов/месяц

### OpenRouteService API
1. Перейти: https://openrouteservice.org/
2. Зарегистрироваться (бесплатно)
3. Перейти в раздел "Tokens"
4. Скопировать ключ
5. Бесплатный лимит: 2,000 запросов/день

---

##  ПРОВЕРКА РАБОТЫ

### 1. Проверить backend
```bash
curl http://localhost:8000/health
```

Должен вернуть:
```json
{
  "status": "ok",
  "app": "AI Logistics Platform",
  "version": "1.0.0"
}
```

### 2. Проверить API docs
Открыть: http://localhost:8000/docs

Должна открыться Swagger UI с всеми endpoints.

### 3. Создать тестовый заказ
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "cargo_type": "general",
    "cargo_name": "Электроника",
    "weight_kg": 2000,
    "volume_m3": 10,
    "pickup_address": "Ташкент, ул. Амира Темура 1",
    "pickup_lat": 41.2995,
    "pickup_lng": 69.2401,
    "delivery_address": "Самарканд, ул. Регистан 1",
    "delivery_lat": 39.6542,
    "delivery_lng": 66.9597,
    "pickup_date": "2026-08-10T10:00:00",
    "urgency_score": 5,
    "budget_uzs": 1500000
  }'
```

### 4. Выполнить AI matching
```bash
curl -X POST http://localhost:8000/api/v1/matching/ \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "top_k": 5
  }'
```

---

##  РАЗРАБОТКА

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Изменения в коде автоматически перезагружают сервер.

### Frontend
```bash
cd frontend
npm start
```

Hot reload работает автоматически.

### Telegram Mini App
```bash
cd telegram-miniapp
npm start
```

---

##  ПРОИЗВОДСТВЕННЫЙ ДЕПЛОЙ

### 1. Собрать образы
```bash
docker-compose build
```

### 2. Настроить production .env
```env
DATABASE_URL=postgresql://user:password@production-db:5432/logistics
REDIS_URL=redis://production-redis:6379/0
SECRET_KEY=very-long-random-secret-key
DEBUG=false
CORS_ORIGINS=https://your-domain.com
```

### 3. Запустить
```bash
docker-compose -f docker-compose.yml up -d
```

### 4. Настроить Nginx
Отредактировать `nginx.conf` для production домена.

---

##  ПОЛЕЗНЫЕ КОМАНДЫ

### Просмотр логов
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Перезапуск сервиса
```bash
docker-compose restart backend
```

### Остановка всех сервисов
```bash
docker-compose down
```

### Остановка с удалением volumes
```bash
docker-compose down -v
```

### Вход в контейнер
```bash
docker-compose exec backend bash
docker-compose exec postgres psql -U postgres -d logistics
```

---

##  ПОИСК И УСТРАНЕНИЕ НЕПОЛАДОК

### Backend не запускается
```bash
# Проверить логи
docker-compose logs backend

# Проверить подключение к БД
docker-compose exec backend python -c "from app.core.database import engine; print(engine.connect())"
```

### Frontend не видит backend
- Убедитесь что `REACT_APP_API_URL` установлен правильно
- Проверьте CORS настройки в backend

### API ключи не работают
- Проверьте что ключи скопированы без пробелов
- Убедитесь что лимиты не превышены
- Проверьте ограничения по доменам (для Яндекс)

---

##  ДОПОЛНИТЕЛЬНЫЕ РЕСУРСЫ

- **API Documentation:** http://localhost:8000/docs
- **Database Schema:** `backend/app/models/`
- **Service Logic:** `backend/app/services/`
- **Frontend Components:** `frontend/src/pages/`

---

##  ПОДДЕРЖКА

Если возникли проблемы:
1. Проверьте логи: `docker-compose logs`
2. Убедитесь что все API ключи установлены
3. Проверьте что порты не заняты
4. Перезапустите сервисы: `docker-compose restart`

---

**Версия:** 1.0  
**Последнее обновление:** 6 августа 2026
