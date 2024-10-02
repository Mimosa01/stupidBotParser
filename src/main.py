import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from commands import COMMANDS
from handlers import handlers

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_router(handlers)
ALLOWED_UPDATES = ['message']


async def main() -> None:
    """
    Функция запускает бота и программно добавляет ему команды меню

    :return: None
    """
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=COMMANDS, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
