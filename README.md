# AI Smart Logistics Platform
## National Transport Hackathon 2026 — Track 2 (E-Logistika)

Полноценная AI-платформа для умных грузоперевозок в Узбекистане.

## Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                         │
│   Dashboard | Orders | Matching | Safety | Routing | Docs   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY (FastAPI)                      │
│   Authentication | Rate Limiting | Logging | CORS           │
─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
         ┌────▼────┐    ┌────▼────┐    ┌─────▼─────┐
         │Business │    │  ML     │    │Integration│
         │  Logic  │    │Services │    │  Layer    │
         └─────────┘    ─────────┘    └───────────
                              │
                  ┌───────────┼───────────┐
                  │           │           │
           ┌──────▼──┐ ┌─────▼────┐ ┌───▼──────┐
           │PostgreSQL│ │  Redis   │ │External  │
           │          │ │  Cache   │ │  APIs    │
           ──────────┘ └──────────┘ ──────────┘
```

## Модули

### 1. Smart Matching
AI-подбор идеального водителя для груза. XGBoost модель, 15+ признаков.

### 2. Cargo Safety Checker
Автоматическая проверка безопасности груза. NLP для сертификатов, ADR классификация.

### 3. AI Route Validator
Построение маршрутов с учётом ограничений для грузов. Интеграция с Яндекс, OpenWeatherMap, OpenRouteService.

### 4. Document Management
Управление ЭТТН, путевыми листами, сертификатами. Автоматическая генерация списков документов.

### 5. Permit Management
Управление рухсатнома. Мониторинг квот, прогнозирование дефицита.

### 6. Telegram Mini App
Мобильный интерфейс для водителей через Telegram.

## Быстрый старт

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Telegram Mini App
cd telegram-miniapp
npm install
npm run dev
```

## Tech Stack

- **Backend:** Python 3.11, FastAPI, SQLAlchemy, XGBoost, TensorFlow
- **Frontend:** React 18, TypeScript, Tailwind CSS, Zustand, React Query
- **Database:** PostgreSQL 15, Redis 7
- **External:** Yandex Maps API, OpenWeatherMap, OpenRouteService
- **DevOps:** Docker, Docker Compose, Nginx
- **Telegram:** Telegram Web App SDK
