from clarifai.rest import ClarifaiApp
from random import randint
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

import settings


def get_bot_number(user_number):
    return randint(user_number - 10, user_number + 10)


def play_random_numbers(user_number, bot_number):
    if user_number > bot_number:
        message = f"Ваше число {user_number}, мое {bot_number}, вы выиграли"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, мое {bot_number}, ничья"
    else:
        message = f"Ваше число {user_number}, мое {bot_number}, вы проиграли"
    return message


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Прислать котика', KeyboardButton('Мои координаты', request_location=True), 'Заполнить анкету']
    ])


def is_cat(file_name):
    app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)
    model = app.public_models.general_model
    responce = model.predict_by_filename(file_name, max_concepts=5)
    if responce['status']['code'] == 10000:
        for concept in responce['outputs'][0]['data']['concepts']:
            if concept['name'] == 'cat':
                return True
    return False


def cat_rating_inline_keyboard(image_name):
    callback_text = f"rating|{image_name}|"
    keyboard = [
        [
            InlineKeyboardButton('Нравится', callback_data=callback_text + '1'),
            InlineKeyboardButton('Не нравится', callback_data=callback_text + '-1')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


if __name__ == "__main__":
    print(is_cat("images/cat1.jpg"))
    print(is_cat("images/not_cat.jpg"))
