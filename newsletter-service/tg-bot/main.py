import telebot
from flask import Flask, request, jsonify
import threading
import base64
from io import BytesIO
from PIL import Image
from flask_cors import CORS
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask_socketio import SocketIO, emit
import logging

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Телеграм токен и пользовательский ID
TELEGRAM_TOKEN = '7304368665:AAHaDslyPe06nmsvihiK9AKbrRWIv6FAEDA'
USER_ID = '301979941'

# Создаем бота и Flask приложение
logging.info("Создаем экземпляр бота и Flask-приложения")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)
CORS(app)

# Настраиваем SocketIO с CORS
socketio = SocketIO(app, cors_allowed_origins="*")

# Функция для сохранения изображения
def save_image(image_data):
    logging.info("Сохраняем изображение")
    image_data = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    image_path = "screenshot.png"
    image.save(image_path)
    logging.info(f"Изображение сохранено в {image_path}")
    return image_path

# Функция для создания кнопок согласования
def create_rating_buttons():
    logging.info("Создаем кнопки согласования")
    keyboard = InlineKeyboardMarkup()
    like_button = InlineKeyboardButton("Согласовать", callback_data="like")
    dislike_button = InlineKeyboardButton("Отказать", callback_data="dislike")
    keyboard.add(like_button, dislike_button)
    return keyboard

# Маршрут для отправки сообщения
@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message', 'Тестовое сообщение!')
    image_data = data.get('image')
    initial_request = data.get('initialRequest', 'Нет запроса')

    try:
        logging.info(f"Получен запрос на отправку сообщения: {message}")
        formatted_message = (
            f"__Запрос на генерацию:__ {initial_request}\n"
            f"__Комментарий пользователя:__ {message}"
        )

        if image_data:
            image_path = save_image(image_data)
            with open(image_path, 'rb') as image_file:
                logging.info("Отправляем фото с сообщением")
                sent_message = bot.send_photo(
                    USER_ID,
                    image_file,
                    caption=formatted_message,
                    reply_markup=create_rating_buttons(),
                    parse_mode='Markdown'
                )
        else:
            logging.info("Отправляем текстовое сообщение")
            sent_message = bot.send_message(
                USER_ID,
                formatted_message,
                reply_markup=create_rating_buttons(),
                parse_mode='Markdown'
            )

        return jsonify({'success': True, 'message': 'Сообщение отправлено!', 'message_id': sent_message.message_id}), 200
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Обработчик обратного вызова для кнопок согласования
@bot.callback_query_handler(func=lambda call: call.data in ["like", "dislike"])
def handle_rating_callback(call):
    user_id = call.from_user.id
    rating = call.data
    message_id = call.message.message_id 
    result_message = "Данные переданы оператору." if rating == "like" else "Данные переданы оператору."
    
    logging.info(f"Получен ответ на согласование: {rating} от пользователя {user_id}")
    
    bot.send_message(user_id, result_message)

    try:
        logging.info("Отправляем обновление через WebSocket")
        socketio.emit('rating_update', {
            'message_id': message_id,
            'rating': rating,
        })
    except Exception as e:
        logging.error(f"Ошибка при отправке оценки через WebSocket: {e}")

# Маршрут для обновления рейтинга
@app.route('/update-rating', methods=['POST'])
def update_rating():
    data = request.json
    message_id = data.get('message_id')
    rating = data.get('rating')

    logging.info(f"Обновляем рейтинг сообщения {message_id} на {rating}")

    socketio.emit('rating_update', {
        'message_id': message_id,
        'rating': rating
    })

    return jsonify({'success': True, 'message': 'Рейтинг обновлен'}), 200

# Функция для запуска бота в отдельном потоке
def start_bot():
    logging.info("Запуск Telegram-бота")
    bot.polling()

@app.route('/')
def home():
    return "Welcome to the Telegram Bot server!"


if __name__ == '__main__':
    logging.info("Запуск приложения")
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()
    
    # Запуск Flask-приложения с SocketIO
    socketio.run(app, host='0.0.0.0', port=5000)
