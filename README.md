# Mini-CRM: Lead Distribution System

Автоматическое распределение лидов между операторами на основе весов и ограничений по нагрузке.

## Быстрый старт

```bash
poetry install

# Загрузка тестовых данных (операторы, источники, лиды, обращения)
poetry run python seed_data.py

poetry run uvicorn src.main:app --reload

poetry shell
uvicorn src.main:app --reload

docker compose up --build
```

**API документация:** http://localhost:8000/docs

## Основные сущности

- **Lead** — клиент (идентифицируется по `external_id`)
- **Source** — канал обращения (Telegram, WhatsApp и т.д.)
- **Operator** — сотрудник с ограничением `max_load`
- **Appeal** — обращение лида через источник
- **OperatorSourceWeight** — вес оператора для источника (для распределения)

## API Endpoints

## Алгоритм распределения

При создании обращения:
1. Находим/создаем лида по `external_id`
2. Фильтруем операторов: `is_active=True` + `current_load < max_load`
3. Выбираем случайно по весам: `random.choices(operators, weights=weights)`
4. Если нет доступных — создаем с `operator_id=NULL`

**Пример весов:**
- Оператор A (вес 20) → 20/50 = 40%
- Оператор B (вес 30) → 30/50 = 60%


## Технологии

- **FastAPI** + **SQLAlchemy 2.0** (Mapped style)
- **Pydantic** для валидации
- **SQLite** (легко заменить на PostgreSQL)
- **Poetry** для зависимостей
- **Docker** для развертывания
