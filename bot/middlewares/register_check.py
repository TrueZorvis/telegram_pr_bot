from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bot.db import User


class RegisterCheck(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any]
    ) -> Any:
        session_maker: sessionmaker = data.get('session_maker')
        async with session_maker() as session:
            async with session.begin():
                result = await session.execute(select(User).where(User.user_id == event.from_user.id))
                user: User = result.one_or_none()

                if user is not None:
                    pass
                else:
                    user = User(
                        user_id=event.from_user.id,
                        username=event.from_user.username
                    )
                    await session.merge(user)
                    if isinstance(event, Message):
                        await event.answer('Ты успешно зарегистрирован(а)!')
                    else:
                        await event.message.answer('Ты успешно зарегистрирован(а)!')

        return await handler(event, data)
