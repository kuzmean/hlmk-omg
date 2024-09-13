# Используем официальный базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем утилиту ping (если она необходима для вашего проекта)
RUN apt-get update && apt-get install -y iputils-ping

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Обновляем pip до последней версии и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Gunicorn и gevent для работы с Flask-SocketIO
RUN pip install gunicorn gevent

# Копируем содержимое текущего каталога в контейнер
COPY . .

# Открываем порт для Flask-приложения
EXPOSE 5000

# Запускаем приложение с использованием Gunicorn и gevent для Flask-SocketIO
CMD ["gunicorn", "--worker-class", "gevent", "--bind", "0.0.0.0:5000", "main:app"]


