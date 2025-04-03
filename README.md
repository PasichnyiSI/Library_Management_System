# Library Management System

Цей проєкт — система управління бібліотекою, побудована на **FastAPI**, **SQLAlchemy**, **PostgreSQL** та **Docker**. Проєкт використовує **Alembic** для міграцій бази даних, **Pydantic** для валідації запитів, **pytest** для unit-тестів та **Uvicorn** для запуску серверу.

## Зміст

- [Вимоги](#Вимоги)
- [Структура Проєкту](#Структура-Проєкту)
- [Налаштування середовища](#Налаштування-середовища)
- [Взаємодія з API](#Взаємодія-з-API)
- [Правила валідації запитів в API](#Правила-валідації-запитів-в-API)
- [Тестування](#Тестування)

## Вимоги

1. **Docker** (для контейнеризації)
2. **Docker Compose** (для зручного запуску сервісів)
3. **Python 3.13+** (для локальної розробки та тестування)
4. **.env файл** для налаштування змінних середовища

## Структура Проєкту

Проєкт складається з кількох основних частин:

- `app/`: Основна частина програми, яка містить всю логіку.
  - `main.py`: Головний файл, що ініціалізує FastAPI додаток.
  - `database.py`: Містить налаштування для підключення до бази даних.
  - `models.py`: Опис моделей для бази даних (наприклад, книги, користувачі).
  - `schemas.py`: Визначає схеми для обміну даними (наприклад, Pydantic моделі).
  - `utils.py`: Містить процеси створення токену доступу та шифрування пароля.
- `routers/`: Частина програми, яка містить всі API-методи.
  - `books.py`: Містить маршрути, які обробляють запити для управління книгами в системі.
  - `authors.py`: Містить маршрути, які обробляють запити для управління авторами в системі.
  - `genres.py`: Містить маршрути, які обробляють запити для управління жанрами в системі.
  - `publishers.py`: Містить маршрути, які обробляють запити для управління видавництвами в системі.
  - `borrowers.py`: Містить маршрути, які обробляють запити для управління читачів в системі.
  - `borrowing_history.py`: Містить маршрути, які обробляють запити для управління записами взятих книжок в системі.
  - `auth.py`: Містить маршрути, які обробляють запити для управління автентифікацією в системі.
- `tests/`: Частина програми, яка містить всі тести.
- `Dockerfile`: Налаштування для Docker.
- `docker-compose.yml`: Налаштування для Docker Compose.
- `alembic.ini`: Файл налаштування Alembic.
- `requirements.txt`: Список залежностей Python для проєкту.
- `openapi.json`: Згенерований файл документації OpenAPI у форматі JSON.
- `openapi.yaml`: Згенерований файл документації OpenAPI у форматі YAML.

## Налаштування середовища

### Крок 1: Клонування репозиторію

Спочатку клонувати репозиторій на вашу локальну машину:

```bash
git clone https://github.com/PasichnyiSI/Library_Management_System.git
cd library-management-system
```
### Крок 2: Налаштування Docker середовища

У репозиторії вже є налаштування для Docker та Docker Compose, тому ви можете легко налаштувати середовище для запуску всіх необхідних контейнерів.

### Крок 3: Налаштування середовища (файл .env)

Створіть файл .env в корені проєкту і додайте наступні змінні середовища:
```env
DATABASE_URL_lms=postgresql://library_user:library_password@db:5432/library_db

SECRET_KEY=mysecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
Ці змінні використовуються для налаштування підключення до бази даних та параметрів аутентифікації.

### Крок 4: Створення та запуск контейнерів

Запустіть Docker Compose, щоб створити та запустити контейнери для вашого додатку та бази даних:

```bash
docker-compose up --build
```
Ця команда автоматично створить два контейнери:
 - library_db: Контейнер з базою даних PostgreSQL.
 - library_app: Контейнер для вашого FastAPI додатку.

### Крок 5: Міграції бази даних (Опціонально)

Щоб застосувати міграції до вашої бази даних, використовуйте Alembic. Спочатку потрібно запустити контейнер для виконання міграцій:

```bash
docker-compose exec app alembic init app/migrations
```
Після чого потрібно перейти до створеної теки й змінити конфігураційний файл migrations/env.py

Замість:

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None
```

Зробити:

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.database import Base
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL_lms")

if not database_url:
    raise ValueError("DATABASE_URL не знайдено в .env!")

config = context.config
config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
```
Зміни зберегти.
Далі треба виконати команду застосування міграції бази даних.

```bash
docker-compose exec app alembic upgrade head
```
Це застосує останні міграції бази даних.

Корисні команди:

Для перевірки таблиць:

```bash
docker-compose exec db psql -U library_user -d library_db -c "\dt"
```

Для ініціалізації нової міграції

```bash
docker-compose exec app alembic revision --autogenerate -m "Initial migration"
```

## Взаємодія з API

Swagger UI автоматично генерується і надається для вашого FastAPI додатку. Після запуску сервера, ви можете отримати доступ до документації API за адресою:

```bash
http://localhost:8000/docs
```

Документація дозволяє вам тестувати кінцеві точки API безпосередньо через інтерфейс браузера.

#### Books
- GET /books/: Отримати список всіх книг.
- POST /books/: Додати нову книгу.
- GET /books/{book_id}: Отримати деталі конкретної книги за її ID.
- DELETE /books/{book_id}: Видалити книгу.
- GET /books/books/{book_id}/history: Отримати історію записів позичання конкретної книги.

#### Authors
- GET /authors/: Отримати список всіх авторів.
- POST /authors/: Додати нового автора.
- GET /authors/{author_id}: Отримати деталі конкретного автора за його ID.
- DELETE /authors/{author_id}: Видалити автора.
- GET /authors/{author_id}/books: Отримати всі книги конкретного автора.

#### Genres
- GET /genres/: Отримати список всіх жанрів.
- POST /genres/: Додати новий жанр.
- GET /genres/{genre_id}: Отримати деталі конкретного жанра за його ID.
- DELETE /genres/{genre_id}: Видалити жанр.

#### Publishers
- GET /publishers/: Отримати список всіх видавництв.
- POST /publishers/: Додати нове видавництво.
- GET /publishers/{publisher_id}: Отримати деталі конкретного видавництва за його ID.
- DELETE /publishers/{publisher_id}: Видалити видавництво.

#### Borrowers
- GET /borrowers/: Отримати список всіх читачів.
- POST /borrowers/: Додати нового читача.
- GET /borrowers/{borrower_id}: Отримати деталі конкретного читача за його ID.
- DELETE /borrowers/{borrower_id}: Видалити читача.

#### Borrowing History
- GET /borrowing_history/: Отримати список всіх записів про взяття книжок.
- POST /borrowing_history/: Додати новий запис про взяття книжки.
- GET /borrowing_history/{record_id}: Отримати деталі конкретного запису за його ID.
- DELETE /borrowing_history/{record_id}: Видалити запис.
- PUT /borrowing_history/{borrowing_id}/return: Повернути книгу по ID запису взяття цієї книги.

#### Authentication
- GET /register: Зареєструвати користувача.
- POST /login: Увійти в обліковий запис для отримання токену доступу.

## Правила валідації запитів в API

Данна бібліотична система для валідації запитів використовуються схеми Pydantic, які забезпечують перевірку коректності вхідних даних для кожного API-методу. Валідація допомагає запобігти неправильним або неповним даним, що можуть бути передані в запитах.

Ось опис основних правил валідації для запитів до API:

1. Створення книги (POST /books/)

Для створення нової книги користувач повинен передати в тілі запиту такі параметри:

```json
{
  "title": "string",
  "isbn": "string",
  "published_year": 2025,
  "author_name": "string",
  "genre_name": "string",
  "publisher_name": "string"
}
```

  - title: Обов'язкове поле. Має бути рядком (string) довжиною не менше 1 символа.
  - isbn: Обов'язкове поле. Має бути рядком (string) та відповідати міжнародним стандартам книжкових номерів.
  - published_year: Обов'язкове поле. Має бути цілим числом (integer), яке вказує рік публікації книги. Має бути не пізніше поточного року.
  - author_name: Обов'язкове поле. Має бути рядком (string) довжиною не менше 1 символа.
  - genre_name: Обов'язкове поле. Має бути рядком (string) довжиною не менше 1 символа.
  - publisher_name: Обов'язкове поле. Має бути рядком (string) довжиною не менше 1 символа.

Приклад валідації:

  - Якщо параметр title порожній або не є рядком, сервер поверне помилку 422.
  - Якщо published_year не є цілим числом або знаходиться поза допустимим діапазоном, сервер поверне помилку 422.
  - Якщо isbn не відповідає стандартам, сервер поверне помилку 422.

2. Видалення книги (POST /books/)

Для видалення книги користувач повинен передати book_id в тілі запиту ID книги. Це обов'язкове (integer) поле. Якщо база даних не має відповідного ID у таблиці книжок, то сервер поверне помилку 404.

## Тестування

Проєкт використовує pytest для тестування. Щоб запустити тести, виконайте наступну команду:

```bash
docker-compose exec app pytest
```

Це запустить всі тести, визначені у цьому проєкті, і виведе результат у термінал.





