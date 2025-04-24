from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_gender_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужчина"), KeyboardButton(text="Женщина")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_level_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Начинающий"), KeyboardButton(text="Продвинутый")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )