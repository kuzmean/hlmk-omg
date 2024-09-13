# Используем официальный базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем утилиту ping
RUN apt-get update && apt-get install -y iputils-ping

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое текущего каталога в контейнер
COPY . .

# Открываем порт для Flask-приложения
EXPOSE 5000

# Запускаем приложение с использованием Flask-SocketIO и eventlet
CMD ["python", "main.py"]


