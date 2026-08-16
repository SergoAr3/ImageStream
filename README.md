# 🖼️ ImageStream

**ImageStream** — сервис для потоковой обработки метаданных изображений с использованием **MinIO**, **Redis** и **PostgreSQL**.

Приложение получает список изображений из MinIO, помещает информацию о них в очередь Redis, а затем отдельный поток считывает данные из Redis и сохраняет метаданные изображений в PostgreSQL.

Проект демонстрирует работу с объектным хранилищем, очередью сообщений, многопоточностью, PostgreSQL, SQLAlchemy и Docker.

---

## ✨ Возможности

- 📦 получение объектов из MinIO;
- 🖼 чтение метаданных изображений;
- 📤 помещение данных об изображениях в Redis;
- 📥 чтение данных из Redis;
- 🗄 сохранение метаданных изображений в PostgreSQL;
- 🧵 параллельная обработка через `Thread` и `Timer`;
- 🏗 разделение логики на сервисы и репозитории;
- 🔄 миграции базы данных через Alembic;
- 🐳 запуск всей инфраструктуры через Docker Compose;
- 📝 логирование процессов через Loguru.

---

## 🛠 Стек технологий

| Технология | Назначение |
|---|---|
| Python | Основной язык проекта |
| PostgreSQL | Хранение метаданных изображений |
| SQLAlchemy 2 | ORM для работы с базой данных |
| psycopg2 | PostgreSQL-драйвер |
| Redis | Очередь между этапами обработки |
| MinIO | Объектное хранилище изображений |
| Alembic | Миграции базы данных |
| Loguru | Логирование |
| python-dotenv | Работа с переменными окружения |
| Docker | Контейнеризация |
| Docker Compose | Запуск PostgreSQL, Redis, MinIO и приложения |

---

## 📁 Структура проекта

```text
ImageStream/
├── config/
│   ├── __init__.py
│   └── settings.py             # Настройки PostgreSQL, Redis и MinIO
│
├── migrations/                 # Alembic migrations
│
├── src/
│   ├── core/
│   │   ├── repositories/       # Абстракции репозиториев
│   │   └── services/
│   │       └── image_service.py
│   │
│   ├── db/                     # SQLAlchemy модели и подключение к БД
│   │
│   ├── repositories/
│   │   ├── image_repo.py       # Работа с PostgreSQL
│   │   ├── minio_repo.py       # Работа с MinIO
│   │   └── redis_repo.py       # Работа с Redis
│   │
│   └── service_provider.py     # Создание зависимостей сервиса
│
├── main.py                     # Точка входа
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── Makefile
├── alembic.ini
├── requirements.txt
└── test.py
```

---

## 🔄 Как работает приложение

Обработка изображений состоит из двух основных этапов.

```text
                ┌───────────────┐
                │     MinIO     │
                │   Images      │
                └───────┬───────┘
                        │
                        ▼
              fetch_images()
                        │
                        ▼
                ┌───────────────┐
                │     Redis     │
                │     Queue     │
                └───────┬───────┘
                        │
                        ▼
               get_images()
                        │
                        ▼
                ┌───────────────┐
                │  PostgreSQL   │
                │ Image metadata│
                └───────────────┘
```

### Первый поток

Метод:

```python
fetch_images()
```

получает объекты из MinIO.

Для каждого изображения создаются данные:

```json
{
  "name": "image.jpg",
  "size": "120.45 KB"
}
```

После этого информация сериализуется в JSON и помещается в Redis.

---

### Второй поток

Метод:

```python
get_images()
```

извлекает данные из Redis.

На основе полученной информации создается объект изображения:

```python
Image(
    title=image_name,
    recording_time=datetime.datetime.now(),
    size=image_size
)
```

После чего метаданные сохраняются в PostgreSQL.

---

## 🧵 Многопоточность

В `main.py` используются два потока.

Первый поток запускает получение изображений из MinIO:

```python
Thread(
    target=fetch_images,
    name="fetch_images"
)
```

Второй процесс запускается с небольшой задержкой:

```python
Timer(
    1,
    get_images
)
```

Таким образом, один поток выступает в роли **producer**, а второй — **consumer**.

```text
Producer                    Consumer
   │                           │
   ▼                           ▼
MinIO ─────► Redis Queue ─────► PostgreSQL
```

---

## 📦 MinIO

MinIO используется как S3-совместимое объектное хранилище.

Приложение получает все объекты из указанного bucket и считывает их метаданные.

Настройки MinIO задаются через переменные окружения:

```env
MINIO_ACCESS_KEY=...
MINIO_SECRET_KEY=...
MINIO_ENDPOINT=...
MINIO_BUCKET_NAME=...
```

Пример для Docker:

```env
MINIO_ACCESS_KEY=sergo
MINIO_SECRET_KEY=your_password
MINIO_ENDPOINT=minio:9000
MINIO_BUCKET_NAME=images
```

---

## 🔴 Redis

Redis используется как промежуточная очередь между MinIO и PostgreSQL.

Схема:

```text
MinIO
  │
  ▼
Producer
  │
  ▼
Redis
  │
  ▼
Consumer
  │
  ▼
PostgreSQL
```

Настройки:

```env
REDIS_HOST=redis
REDIS_PORT=6379
```

---

## 🐘 PostgreSQL

PostgreSQL используется для хранения метаданных изображений.

В базе сохраняются данные вроде:

```text
title
recording_time
size
```

Подключение задается через:

```env
DATABASE_URL=...
```

Например:

```env
DATABASE_URL=postgresql+psycopg2://postgres:your_password@db:5432/image_stream
```

---

## 🔐 Переменные окружения

Создайте `.env` в корне проекта.

Пример:

```env
DATABASE_URL=postgresql+psycopg2://postgres:your_password@db:5432/image_stream

REDIS_HOST=redis
REDIS_PORT=6379

MINIO_ACCESS_KEY=sergo
MINIO_SECRET_KEY=your_password
MINIO_ENDPOINT=minio:9000
MINIO_BUCKET_NAME=images
```

> Не добавляйте `.env`, пароли или другие секреты в GitHub.

---

## 🐳 Запуск через Docker

В проекте используется Docker Compose.

Запускаются четыре сервиса:

```text
Redis
PostgreSQL
MinIO
ImageStream
```

Запуск:

```bash
docker compose up --build
```

Запуск в фоне:

```bash
docker compose up -d --build
```

Просмотр логов:

```bash
docker compose logs -f
```

Остановка:

```bash
docker compose down
```

---

## 🌐 MinIO Console

После запуска Docker Compose MinIO доступен на портах:

```text
9000 — MinIO API
9001 — MinIO Console
```

Веб-интерфейс:

```text
http://localhost:9001
```

После входа необходимо создать bucket, соответствующий значению:

```env
MINIO_BUCKET_NAME
```

Например:

```text
images
```

После этого можно загрузить изображения через веб-интерфейс MinIO.

---

## 🚀 Локальный запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/SergoAr3/ImageStream.git
cd ImageStream
```

---

### 2. Создание виртуального окружения

```bash
python -m venv venv
```

Linux / macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

---

### 4. Настройка `.env`

Для локального запуска сервисов:

```env
DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/image_stream

REDIS_HOST=localhost
REDIS_PORT=6380

MINIO_ACCESS_KEY=sergo
MINIO_SECRET_KEY=your_password
MINIO_ENDPOINT=localhost:9000
MINIO_BUCKET_NAME=images
```

---

### 5. Применение миграций

```bash
alembic upgrade head
```

или:

```bash
make migrate
```

---

### 6. Запуск приложения

```bash
python main.py
```

---

## 🗄 Миграции

Для управления схемой PostgreSQL используется Alembic.

Применение миграций:

```bash
alembic upgrade head
```

или:

```bash
make migrate
```

Создание новой миграции:

```bash
make migration NAME="migration_name"
```

---

## 🧩 Архитектура

В проекте используется разделение на несколько слоев:

```text
Core
 │
 ├── Services
 └── Repository interfaces

Infrastructure
 │
 ├── PostgreSQL repository
 ├── Redis repository
 └── MinIO repository

Application
 │
 └── ImageService
```

`ImageService` не работает напрямую с PostgreSQL, Redis или MinIO.

Вместо этого он получает реализации репозиториев:

```python
ImageService(
    image_repository,
    minio_repository,
    redis_repository
)
```

Это позволяет отделить бизнес-логику от инфраструктуры.

---

## 🔌 Repository Pattern

Для разных источников данных используются отдельные репозитории.

### MinIO Repository

Отвечает за получение изображений:

```text
src/repositories/minio_repo.py
```

### Redis Repository

Отвечает за работу с очередью:

```text
src/repositories/redis_repo.py
```

### Image Repository

Отвечает за сохранение метаданных:

```text
src/repositories/image_repo.py
```

Такое разделение делает код более модульным и упрощает замену отдельных компонентов.

---

## 📦 Основные зависимости

```text
SQLAlchemy
psycopg2
MinIO
Redis
Alembic
Loguru
python-dotenv
```

Полный список находится в:

```text
requirements.txt
```
