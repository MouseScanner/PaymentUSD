# PaymentAPI

Высокопроизводительный сервис обработки платежей с поддержкой USDT.

## Технический стек

- **Tornado** - асинхронный веб-фреймворк
- **PostgreSQL** - основная база данных  
- **Celery + Redis** - очереди задач
- **SQLAlchemy** - ORM

## Основной функционал

- Создание и управление аккаунтами
- Переводы между аккаунтами
- Обработка платежей в USDT
- Асинхронная обработка транзакций

## Быстрый старт

```bash
# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp .env.example .env

# Миграции базы данных
alembic upgrade head

# Запуск Redis
redis-server

# Запуск Celery
celery -A app.worker worker --loglevel=info

# Запуск приложения
python app/main.py
```

## API Endpoints

- `POST /accounts` - создание аккаунта
- `GET /accounts/{id}` - информация об аккаунте
- `POST /transfers` - перевод между аккаунтами
- `GET /transfers/{id}` - статус перевода

## Архитектура

Проект следует принципам чистой архитектуры с разделением на слои:
- Handlers (API)
- Services (бизнес-логика)
- Models (данные)
- Utils (вспомогательные функции) 