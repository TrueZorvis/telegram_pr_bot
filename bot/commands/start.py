from aiogram import types
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder, KeyboardButton, KeyboardButtonPollType
)
# from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
# from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup


async def start(message: types.Message) -> None:
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.button(text='Помощь')
    menu_builder.add(
        KeyboardButton(text='Отправить контакт', request_contact=True)
    )
    menu_builder.row(
        KeyboardButton(text='Отправить голосование', request_poll=KeyboardButtonPollType())
    )

    await message.answer(
        'Меню',
        # 1-й способ добавления кнопок
        reply_markup=menu_builder.as_markup(resize_keyboard=True)
        # 2-й способ добавления кнопок
        # reply_markup=ReplyKeyboardMarkup(keyboard=menu_builder.export())
    )


