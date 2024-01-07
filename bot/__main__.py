import os
import asyncio
import logging
import pathlib

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from aioredis import Redis
from sqlalchemy.engine import URL

from bot.handlers import register_user_commands
from bot.handlers.bot_commands import bot_commands
from bot.middlewares.register_check import RegisterCheck

from db import create_async_engine, get_session_maker


async def bot_start(logger: logging.Logger) -> None:
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    redis = Redis(
        host=os.getenv('REDIS_HOST') or '127.0.0.1',
        password=os.getenv('REDIS_PASSWORD') or None,
        username=os.getenv('REDIS_USER') or None,
    )

    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())

    bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')
    await bot.set_my_commands(commands=commands_for_bot)
    register_user_commands(dp)

    postgres_url = URL.create(
        "postgresql+asyncpg",
        username=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        database=os.getenv('POSTGRES_DB')
    )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    # Делегировано alembic
    # await proceed_schemas(async_engine, BaseModel.metadata)
    await dp.start_polling(bot, session_maker=session_maker, logger=logger, redis=redis)


def setup_env():
    """Настройка переменных окружения"""
    from dotenv import load_dotenv
    path = pathlib.Path(__file__).parent.parent
    dotenv_path = path.joinpath('.env')
    if dotenv_path.exists():
        load_dotenv(dotenv_path)


def main():
    """Для запуска через poetry"""
    logger = logging.getLogger(__name__)
    try:
        setup_env()
        asyncio.run(bot_start(logger))
        logger.info('Bot started')
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')


if __name__ == '__main__':
    main()
