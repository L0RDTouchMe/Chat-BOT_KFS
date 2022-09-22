from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


info_inline_btn_1 = InlineKeyboardButton(
    'Удалить!!!', callback_data='delete'
    )
info_inline_btn_2 = InlineKeyboardButton(
    'Редактировать!!!', callback_data='redact'
    )
info_inline_btn_3 = InlineKeyboardButton(
    'Отмена', callback_data='cancel'
    )


inline_admin_keyboard = InlineKeyboardMarkup().add(info_inline_btn_1).add(info_inline_btn_2).add(info_inline_btn_3)
