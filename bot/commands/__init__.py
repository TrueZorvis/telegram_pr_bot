__all__ = ['register_user_commands']

from aiogram import Router
from aiogram.filters import CommandStart
from bot.commands.start import start


def register_user_commands(router: Router) -> None:
    router.message.register(start, CommandStart())
