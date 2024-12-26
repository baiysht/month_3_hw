from pyexpat.errors import messages

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import main_db


class EditProduct(StatesGroup):
    for_field = State()
    for_new_photo = State()
    for_new_field = State()



async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    button_all_products = types.InlineKeyboardButton('Вывести все товары',
                                                     callback_data='edit_all_products')

    button_one_products = types.InlineKeyboardButton('Вывести по одному',
                                                     callback_data='edit_one_products')

    keyboard.add(button_all_products, button_one_products)

    await message.answer('Выберите как просмотреть товары: ', reply_markup=keyboard)



async def send_all_products(call: types.CallbackQuery):
    products = main_db.fetch_all_products()

    if products: # True
        for product in products:
            caption = (f'Название - {product["name_product"]}\n'
            f'Размер - {product["product_size"]}\n'
            f'Категория - {product["category"]}\n'
            f'Артикул - {product["productid"]}\n'
            f'Информация о товаре - {product["infoproduct"]}\n'
            f'Коллекция товара - {product["collection"]}\n'
            f'Цена - {product["price"]}\n')

            edit_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
            edit_keyboard.add(InlineKeyboardButton('Редактировать',
                                                   callback_data=f'edit_{product["productid"]}'))

            await call.message.answer_photo(photo=product['photo'], caption=caption,
                                            reply_markup=edit_keyboard)
    else: # False
        await call.message.answer('База пустая! Товаров нет.')


async def edit_products(call: types.CallbackQuery, state: FSMContext):
    productid = int(call.data.split('_')[1])

    await state.update_data(productid=productid)

    keyboard = InlineKeyboardMarkup(row_width=2)

    name_button = InlineKeyboardButton(text="Название", callback_data="field_name_product")
    category_button = InlineKeyboardButton(text="Категория", callback_data="field_category")
    price_button = InlineKeyboardButton(text="Цена", callback_data="field_price")
    size_button = InlineKeyboardButton(text="Размер", callback_data="field_size")
    photo_button = InlineKeyboardButton(text="Фото", callback_data="field_photo")
    info_button = InlineKeyboardButton(text="Инфо о товаре", callback_data="field_info_product")
    collection_button = InlineKeyboardButton(text="Коллекция товара", callback_data="field_collection")
    keyboard.add(name_button, category_button, price_button, size_button, photo_button, info_button, collection_button)

    await call.message.answer('Выберите поле для редактирования:', reply_markup=keyboard)

    await EditProduct.for_field.set()

async def select_field_product(call: types.CallbackQuery, state: FSMContext):
    field_map = {
        'field_name_product': "name_product",
        'field_category': "category",
        'field_price': "price",
        'field_size': "product_size",
        'field_photo': "photo",
        'field_info_product': "infoproduct",
        'field_collection': "collection"
    }

    field = field_map.get(call.data)

    if not field:
        await call.message.answer('Недопустимое поле!')
        return

    await state.update_data(field=field)

    if field == 'photo':
        await EditProduct.for_new_photo.set()
        await call.message.answer('Отправьте новое фоток:')
    else:
        await EditProduct.for_new_field.set()
        await call.message.answer('Отправьте новое значение:')



async def set_new_values(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    productid = user_data['productid']

    field = user_data['field']

    new_value = message.text

    main_db.update_product_field(productid, field, new_value)

    await message.answer(f'Поле {field} успешно обновлено!')
    await state.finish()

async def set_new_photo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    productid = user_data['productid']
    print(productid)
    photo_id = message.photo[-1].file_id

    main_db.update_product_field(productid, 'photo', photo_id)
    await message.answer('Фото успешно обновлено!')
    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands='edit_product')
    dp.register_callback_query_handler(send_all_products, Text(equals='edit_all_products'))
    dp.register_callback_query_handler(edit_products, Text(startswith='edit_'),
                                       state="*")
    dp.register_callback_query_handler(select_field_product, Text(startswith='field_'),
                                       state=EditProduct.for_field)
    dp.register_message_handler(set_new_values, state=EditProduct.for_new_field)
    dp.register_message_handler(set_new_photo, state=EditProduct.for_new_photo,
                                content_types=['photo'])