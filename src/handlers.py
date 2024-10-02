import os
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from parse import parse


handlers = Router()


class ParseData(StatesGroup):
    list_links = State()
    count_page = State()


@handlers.message(Command('start'))
async def start_bot(message: types.Message):
    await message.answer('Давайте же начнем парсить сайт https://habr.com')


@handlers.message(Command('help'))
async def parsing(message: types.Message):
    await message.answer('Отправьте мне список ссылок на категории сайта. (Каждая ссылка должна быть с новой строки)')


@handlers.message(Command('get'))
async def get_files(message: types.Message):
    directory = 'parse_files'
    files = os.listdir(os.getenv('DIRECTORY'))

    files_upload = [FSInputFile(f'{directory}/{filename}') for filename in files]

    for file in files_upload:
        await message.answer_document(file)


@handlers.message(StateFilter(None), Command('parse'))
async def start_parse(message: types.Message, state: FSMContext):
    await message.answer('Отправьте мне список ссылок на категории сайта. (Каждая ссылка должна быть с новой строки)')
    await state.set_state(ParseData.list_links)


@handlers.message(ParseData.list_links, F.text)
async def start_parse(message: types.Message, state: FSMContext):
    list_link = [link for link in message.text.split('\n') if link.startswith('https://habr.com/')]

    for index, link in enumerate(list_link):
        if not link.endswith('articles/'):
            list_link[index] = f'{link}articles/'

    await state.update_data(list_links=list_link)
    await message.answer('Сколько спарсить страниц?')
    await state.set_state(ParseData.count_page)


@handlers.message(ParseData.count_page, F.text)
async def count_page(message: types.Message, state: FSMContext):
    try:
        count = int(message.text)
        await state.update_data(count_page=count)
        data = await state.get_data()

        await parse(data['list_links'], data['count_page'])
        await message.answer('Готово! Введите /get чтобы получить файлы с информацией.')
    except:
        await message.answer('Нужно ввести число.')
        await state.set_state(ParseData.count_page)
