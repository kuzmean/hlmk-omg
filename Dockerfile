# Используем официальный базовый образ Node.js
FROM node:18

# Создаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем утилиту ping
RUN apt-get update && apt-get install -y iputils-ping

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем остальной код
COPY . .

# Открываем порт для приложения
EXPOSE 3000

# Запускаем приложение
CMD ["npm", "start"]
