import sqlite3
from create_bot import cursor, conn, bot
from keyboards import admin_keyboard, menus_keyboard, create_keyboard, inline_admin_keyboard
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Filter, Command


users = {
    "admin" : "admin"
}

kb_menus = {
    "Напитки": "Drinks",
    "Бургеры": "Burgers",
    "Картофельные блюда" : "potato",
    "Мясные блюда": "meat"
}
# primal_id = []


# FSM машина состояний авторизации
class login(StatesGroup):
    login_start = State()
    login_step_1 = State()
    login_step_3 = State()
    login_step_4 = State()
    login_step_5 = State()
    login_step_6 = State()
    login_step_7 = State()

# Обработчик команды login
async def command_login(message: types.Message):
    await message.reply("Введите логин:")
    await login.login_start.set()

# Авторизация: шаг 1
async def login_step_1(message: types.Message, state: FSMContext):
    # Сохраняем введенный логин в state
    await state.update_data(login=message.text)
    await message.answer("Введите пароль:")
    await login.next()

# Авторизация: шаг 2
async def login_step_2(message: types.Message, state: FSMContext):
    # Сохраняем введенный пароль в state
    await state.update_data(password=message.text)
    data = await state.get_data()
    
    # Проверка есть ли такой пользователь в БД
    if data["login"] in users.keys():
        if data["password"] == users[data["login"]]:
            await message.answer("Добро пожаловать!\nВыбирете действие:", reply_markup=admin_keyboard)
            await login.next()
        else: 
            await message.answer("Неверный пароль")
            await state.finish()
    else: 
        await message.answer("Неверный логин")
        await state.finish()

async def login_step_3(message: types.Message, state: FSMContext):
    if message.text == "Редактировать меню":
        await message.answer("Вы вошли в режим редактирования меню !!!\nВыбирете меню для редактирования", reply_markup=menus_keyboard)
        await login.next()


async def login_step_4(message: types.Message, state: FSMContext):
    if message.text in kb_menus.keys():
        await state.update_data(menu_type=kb_menus[message.text])
        # Делаем запрос в БД
        cursor.execute(f"SELECT Name FROM {kb_menus[message.text]}")
        result = cursor.fetchall()
        # Заполняем массив с едой из текущего меню
        foodArr = []
        for i in result:
            foodArr.append(i[0])
        # Сохраняем массив с едой из текущего меню в памяти
        await state.update_data(foodArr=foodArr)
        # Сохраняем текущую клавиатуру
        await state.update_data(cur_menu_kb=create_keyboard(result))
        data = await state.get_data()
        cur_menu_local = data["cur_menu_kb"]
        await message.answer(f"Выбрано: {message.text}", reply_markup=cur_menu_local)
        await login.next()
    elif message.text == "Выход":
        await message.answer("Вы вышли из аккаунта!\nВведите логин")
        await login.login_start.set()

async def login_step_5(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'Другое меню':
        await message.answer("Выберите другое меню", reply_markup=menus_keyboard)
        await login.login_step_4.set()

    elif message.text == "Выход":
        await message.answer("Вы вышли из аккаунта!\nВведите логин")
        await login.login_start.set()

    elif message.text in data["foodArr"]:
        cursor.execute(f"SELECT * FROM {data['menu_type']} WHERE Name = ?", (message.text,))
        product = cursor.fetchone()
        await message.reply("Название: " + product[1]
                            + "\nСостав: " + str(product[4])
                            + "\nКкал: " + str(product[2])
                            + "\nСкидка: " + str(product[3]), reply_markup=inline_admin_keyboard)
        await login.next()

async def login_step_6(callback_query: types.CallbackQuery, state: FSMContext):
    text = callback_query.data

    if text == "delete":
        await bot.answer_callback_query(
            callback_query.id,
            text='КУДА Я ЖИМАЛ!!!', show_alert=True)

    if text == "redact":
        await bot.answer_callback_query(
            callback_query.id,
            text='СУДА Я ЖИМАЛ!!!', show_alert=True)

    elif callback_query.data == 'cancel':
        print('sdasdasd')
        await login.login_step_7.set()

async def login_step_7(message: types.Message, state: FSMContext):
    print("123123123")
    await message.answer("Отмена\nВыбирете меню для редактирования", reply_markup=menus_keyboard)
    await login.login_step_4.set()


def admin_handlers_register(dp : Dispatcher):
    dp.register_message_handler(
        command_login, 
        Command(['login'])
    )
    dp.register_message_handler(login_step_1, state=login.login_start)
    dp.register_message_handler(login_step_2, state=login.login_step_1)
    dp.register_message_handler(login_step_3, state=login.login_step_3)
    dp.register_message_handler(login_step_4, state=login.login_step_4)
    dp.register_message_handler(login_step_5, state=login.login_step_5)
    dp.register_callback_query_handler(login_step_6, state=login.login_step_6, text=['delete', 'redact', 'cancel'])
    dp.register_message_handler(login_step_7, state=login.login_step_7)
    