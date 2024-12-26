# buttons.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
cancel_button = KeyboardButton("Отмена")
cancel_markup.add(cancel_button)

start_markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
start_markup.add(KeyboardButton('/start'), KeyboardButton('/quiz'), KeyboardButton('/registration'), KeyboardButton('/buy'))

submit = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
submit.add(KeyboardButton("Да"), KeyboardButton('Нет'))