from contextlib import suppress

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select  # type: ignore
from sqlalchemy.orm import sessionmaker, joinedload, selectinload  # type: ignore

from bot.db.user import get_user
from bot.structures.fsm_groups import PostStates
from bot.structures.keyboards import MENU_BOARD
from bot.structures.keyboards.posts_board import generate_posts_board


async def start(message: types.Message) -> Message:
    return await message.answer('Меню', reply_markup=MENU_BOARD)


async def call_start(call: types.CallbackQuery, state: FSMContext) -> Message:
    await state.clear()
    with suppress(Exception):
        await call.message.delete()
    return await call.message.answer('Меню', reply_markup=MENU_BOARD)


async def menu_posts(message: types.Message, session_maker: sessionmaker, state: FSMContext) -> None:
    user = await get_user(user_id=message.from_user.id, session_maker=session_maker)
    await message.answer('Твои посты', reply_markup=generate_posts_board(posts=user.posts))
    await state.set_state(PostStates.waiting_for_select)


async def menu_channels(message: types.Message) -> None:
    pass


async def menu_account(message: types.Message) -> None:
    pass
