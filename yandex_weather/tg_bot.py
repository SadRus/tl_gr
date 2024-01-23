import redis
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from .models import Weather
from django.conf import settings


_database = None


def get_weather_keyboard():
    keyboard = [
        [InlineKeyboardButton('Узнать погоду', callback_data='weather')]
    ]
    return keyboard


def start(update: Update, context: CallbackContext):
    reply_markup = InlineKeyboardMarkup(get_weather_keyboard())
    update.message.reply_text(
        'Здравствуйте! '
        'Вас приветствует бот прогноза погоды.',
        reply_markup=reply_markup,
    )
    return 'HANDLE_WEATHER'


def handle_weather(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Введите название города с большой буквы,\n'
             'составные названия через дефис\n'
             'например: Санкт-Петербург, Ростов-на-Дону, Нижний Новгород'
    )
    return 'HANDLE_CITY'


def handle_city(update: Update, context: CallbackContext):
    city_name = update.message.text
    reply_markup = InlineKeyboardMarkup(get_weather_keyboard())

    if not Weather.objects.filter(city=city_name).exists():
        update.message.reply_text(
            text='Такого города не существует или неправильный формат.\n'
                 'Попробуйте еще раз.',
            reply_markup=reply_markup,
        )
        return 'HANDLE_WEATHER'

    url = 'http://127.0.0.1:8000/api/weather'
    params = {
        'city': city_name,
    }
    response = requests.get(url, params=params)
    response_data = response.json()

    update.message.reply_text(
        text=f'Текущая температура🌡: {response_data["temperature"]}°С\n'
             f'Атмосферное давление📏: {response_data["pressure"]}мм рт.ст.\n'
             f'Скорость ветра💨: {response_data["wind_speed"]}м/с',
        reply_markup=reply_markup,
    )
    return 'HANDLE_WEATHER'


def handle_users_reply(update, context):
    db = get_database_connection()

    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return None

    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = db.get(chat_id).decode("utf-8")

    states_functions = {
        'START': start,
        'HANDLE_CITY': handle_city,
        'HANDLE_WEATHER': handle_weather,
    }
    state_handler = states_functions[user_state]

    try:
        next_state = state_handler(update, context)
        db.set(chat_id, next_state)
    except Exception as err:
        print(err)


def get_database_connection():
    """
    Возвращает соединение с базой данных Redis, либо создаёт новое,
    если онo ещё не созданo.
    """

    global _database
    if _database is None:
        database_host = settings.REDIS_HOST
        database_port = settings.REDIS_PORT
        _database = redis.Redis(host=database_host, port=database_port)
    return _database


def main():
    tg_bot_token = settings.TG_BOT_TOKEN

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
