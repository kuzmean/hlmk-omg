# Используем официальный базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем requirements.txt в рабочую директорию
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы вашего проекта в рабочую директорию
COPY . .

# Открываем порт 5001 для Flask-приложения
EXPOSE 5001

# Устанавливаем Gunicorn
RUN pip install gunicorn

# Команда для запуска приложения с Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "main:app"]
