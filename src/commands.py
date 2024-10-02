from aiogram.types import BotCommand


COMMANDS = [
    BotCommand(command='start', description='Запуск бота'),
    BotCommand(command='help', description='Помощь'),
    BotCommand(command='get', description='Получить файлы'),
    BotCommand(command='parse', description='Начать парсинг'),
]
