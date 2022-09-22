from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

btn_1 = KeyboardButton('Редактировать меню')


admin_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True
)

admin_keyboard.row(btn_1)