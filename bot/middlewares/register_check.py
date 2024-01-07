from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from bot.db.user import is_user_exists, create_user


class RegisterCheck(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any]
    ) -> Any:
        if event.web_app_data:
            return await handler(event, data)

        session_maker = data['session_maker']
        redis = data['redis']
        user = event.from_user

        if not await is_user_exists(user_id=event.from_user.id, session_maker=session_maker, redis=redis):
            await create_user(user_id=event.from_user.id,
                              username=event.from_user.username, session_maker=session_maker, locale=user.language_code)
            await data['bot'].send_message(event.from_user.id, 'Ты успешно зарегистрирован(а)!')

        return await handler(event, data)
