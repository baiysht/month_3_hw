# quiz.py
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot

async def quiz_1(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)

    button2 = InlineKeyboardButton("Вопрос 2", callback_data='quiz_2')
    button3 = InlineKeyboardButton("Вопрос 3", callback_data='quiz_3')
    button4 = InlineKeyboardButton("Вопрос 4", callback_data='quiz_4')

    keyboard.add(button2, button3, button4)

    question = 'XBOX or Sony'
    answer = ['XBOX', 'Sony', 'Nintendo']

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation='Жаль...',
        open_period=60,
        reply_markup=keyboard
    )



async def quiz_2(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)

    button1 = InlineKeyboardButton("Вопрос 1", callback_data='quiz_1')
    button3 = InlineKeyboardButton("Вопрос 3", callback_data='quiz_3')
    button4 = InlineKeyboardButton("Вопрос 4", callback_data='quiz_4')

    keyboard.add(button1, button3, button4)

    question = 'Python, JavaScript, Java, PHP and Swift'
    answer = ['Python', 'JavaScript', 'Java', 'PHP', 'Swift']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=True,
        type='quiz',
        correct_option_id=0,
        explanation='Всё с тобой понятно -_-',
        open_period=60
    )


async def quiz_3(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)

    button1 = InlineKeyboardButton("Вопрос 1", callback_data='quiz_1')
    button2 = InlineKeyboardButton("Вопрос 2", callback_data='quiz_2')
    button4 = InlineKeyboardButton("Вопрос 4", callback_data='quiz_4')

    keyboard.add(button1, button2, button4)

    question = 'Что мне по душе?'
    answer = ['Audi', 'Porsche', 'Volkswagen', 'BMW', 'Mercedes']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=True,
        type='quiz',
        correct_option_id=3,
        explanation='Всё с тобой понятно -_-',
        open_period=60
    )


async def quiz_4(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)

    button1 = InlineKeyboardButton("Вопрос 1", callback_data='quiz_1')
    button2 = InlineKeyboardButton("Вопрос 2", callback_data='quiz_2')
    button3 = InlineKeyboardButton("Вопрос 3", callback_data='quiz_3')

    keyboard.add(button1, button2, button3)

    question = 'Какой двигатель у Порш 911 992'
    answer = ['V6', 'I4', 'V12', 'VR6', 'F6']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=True,
        type='quiz',
        correct_option_id=4,
        explanation='Не-а',
        open_period=60
    )

def register_quiz_handlers(dp: Dispatcher):
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, text='quiz_2')
    dp.register_callback_query_handler(quiz_3, text='quiz_3')
    dp.register_callback_query_handler(quiz_4, text='quiz_4')
