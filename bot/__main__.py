import os
import asyncio
import logging
from aiogram import Bot, Dispatcher

from commands import register_user_commands


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    dp = Dispatcher()
    bot = Bot(token=os.getenv('TOKEN'))

    register_user_commands(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
