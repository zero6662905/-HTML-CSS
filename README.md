# Міграції бази даних з Alembic

## Що таке Alembic

[Alembic](https://alembic.sqlalchemy.org/) – це легкий інструмент для управління **версіями та міграціями бази даних** у проєктах Python, що використовують SQLAlchemy.

Він дозволяє:
- Зберігати стан структури БД під контролем версій.
- Автоматизувати створення, застосування та відкочування міграцій.
- Забезпечувати узгодженість схеми БД при командній роботі та деплої.

## Для чого використовується Alembic

При роботі з FastAPI та SQLAlchemy структура моделей БД змінюється:
- Додаються нові таблиці.
- Додаються / видаляються колонки.
- Змінюються типи колонок.

Всі ці зміни **зручно фіксувати міграціями**, щоб автоматично оновлювати структуру БД у будь-якому середовищі (локально, staging, production).

## Налаштування Alembic

### 1️⃣ Встановлення

```bash
pip install alembic
```
### 2️⃣ Ініціалізація Alembic

```bash
alembic init migrations
```
### 3️⃣ Налаштування alembic.ini
У _alembic.ini_ знайди рядок:

```
sqlalchemy.url = driver://user:pass@localhost/dbname
```
та або заміни на свою URL БД, або використай через settings.py у env.py.

### 4️⃣ Налаштування env.py
У _migrations/env.py_ потрібно імпортувати **Base з твоїх моделей** та підключити URL БД з settings.py.

Наприклад:

```python
...
from settings import api_config  # твій конфіг
from models import animal  # імпортуємо всі моделі

from sqlalchemy.orm import declarative_base

config = context.config
config.set_main_option("sqlalchemy.url", api_config.alembic_uri_sqlite())
target_metadata = animal.Base.metadata  # якщо Base визначений у models/animal.py


def run_migrations_offline():
    ...
def run_migrations_online():
    ...


```
### 5️⃣  Створення міграцій
Автоматичне створення міграцій

`alembic revision --autogenerate -m "create users table"`
Це створить файл у alembic/versions/, де Alembic зафіксує зміни у структурі таблиць.

Перевіряй згенеровані міграції вручну перед застосуванням!

### 6️⃣  Застосування міграцій

```bash
alembic upgrade head
```
або до конкретної версії:

```bash
alembic upgrade <revision_id>
```
### Відкат міграцій
Відкат на одну міграцію назад:

```bash
alembic downgrade -1
```
До конкретної версії:

```bash
alembic downgrade <revision_id>
```

## Основні команди Alembic

| Команда                                           | Опис                                               |
|---------------------------------------------------|----------------------------------------------------|
| `alembic init alembic`                            | Ініціалізувати Alembic у проєкті                  |
| `alembic revision -m "msg"`                       | Створити пусту міграцію                           |
| `alembic revision --autogenerate -m "msg"`        | Створити міграцію з автозаповненням               |
| `alembic upgrade head`                            | Застосувати всі міграції до останньої версії      |
| `alembic downgrade -1`                            | Відкотити одну міграцію назад                     |
| `alembic current`                                 | Показати поточну версію міграції                  |
| `alembic history`                                 | Показати історію міграцій                         |
| `alembic heads`                                   | Показати всі верхівкові ревізії                   |
| `alembic show <revision>`                         | Показати деталі конкретної міграції               |