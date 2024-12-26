# fsm_reg.py
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import cancel_markup, start_markup
from aiogram.types import ReplyKeyboardRemove
from db import main_db

class FSMShop(StatesGroup):
    Modelname = State()
    Productid = State()
    Product_size = State()
    Category = State()
    Price = State()
    Infoproduct = State()
    Collection = State()
    Photo = State()
    Submit = State()


async def start_fsm_shop(message: types.Message):
    await message.answer('Введите название модели:', reply_markup=cancel_markup)
    await FSMShop.Modelname.set()

async def load_modelname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['modelname'] = message.text

    await  FSMShop.next()
    await message.answer('Укажите id товара:', reply_markup=cancel_markup)

async def load_productid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['productid'] = message.text

    await FSMShop.next()
    await message.answer('Укажите свой размер:', reply_markup=cancel_markup)


async def load_product_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_size'] = message.text

    await FSMShop.next()
    await message.answer('Укажите категорию товара:', reply_markup=cancel_markup)


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await FSMShop.next()
    await message.answer('Укажите цену товара:', reply_markup=cancel_markup)


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await FSMShop.next()
    await message.answer('Укажите информацию о товаре:', reply_markup=cancel_markup)

async def load_infopruduct(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['infoproduct'] = message.text

    await FSMShop.next()
    await message.answer('Укажите коллекцию товара:', reply_markup=cancel_markup)


async def load_collection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['collection'] = message.text

    await FSMShop.next()
    await message.answer('Отправьте фотку товара:', reply_markup=cancel_markup)


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    await FSMShop.next()
    await message.answer(f'Верные ли данные?')
    await message.answer_photo(photo=data['photo'],
                               caption=f'Название модели - {data["modelname"]}\n'
                             f'id товара - {data["productid"]}\n'
                             f'Размер - {data["product_size"]}\n'
                             f'Категория - {data["category"]}\n'
                             f'Цена - {data["price"]}\n'
                             f'Иноформация о товаре - {data["infoproduct"]}\n'
                             f'Коллекция - {data["collection"]}'
                               )


async def load_submit(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        async with state.proxy() as data:
            await main_db.sql_insert_shop(
                name_product=data['modelname'],
                product_size=data['product_size'],
                price=data['price'],
                photo=data['photo'],
                productid=data['productid']
            )
            await main_db.sql_insert_product_details(
                productid=data['productid'],
                category=data['category'],
                infoproduct=data['infoproduct']
            )
            await main_db.sql_insert_collection_products(
                productid=data['productid'],
                collection=data['collection']
            )
            await message.answer('Ваши данные в базе!')
            await state.finish()

    elif message.text == 'Нет':
        await message.answer('Хорошо, отменено!')
        await state.finish()

    else:
        await message.answer('Введите Да или Нет!')

async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=start_markup)


def register_fsmshop_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена',
                                                 ignore_case=True), state='*')

    dp.register_message_handler(start_fsm_shop, commands=['buy'])
    dp.register_message_handler(load_modelname, state=FSMShop.Modelname)
    dp.register_message_handler(load_productid, state=FSMShop.Productid)
    dp.register_message_handler(load_product_size, state=FSMShop.Product_size)
    dp.register_message_handler(load_category, state=FSMShop.Category)
    dp.register_message_handler(load_price, state=FSMShop.Price)
    dp.register_message_handler(load_infopruduct, state=FSMShop.Infoproduct)
    dp.register_message_handler(load_collection, state=FSMShop.Collection)
    dp.register_message_handler(load_photo, state=FSMShop.Photo, content_types=['photo'])
    dp.register_message_handler(load_submit, state=FSMShop.Submit)