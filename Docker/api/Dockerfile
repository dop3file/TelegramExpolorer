# Базовый образ Python с той же версией, что и в вашем проекте
FROM python:3.11 as builder

# Установка Poetry
ENV POETRY_VERSION=2.0.0
RUN pip install poetry==${POETRY_VERSION}

# Копируем только файлы, необходимые для установки зависимостей
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости (без root)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Конечный образ
FROM python:3.11-slim

# Установка необходимых системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Копируем установленные зависимости из builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копируем код приложения
WORKDIR /app
COPY . .

# Переменные окружения
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Порт, который будет слушать приложение
EXPOSE 8000