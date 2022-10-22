import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from decouple import config
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import aioschedule
from aiogram import html
from aiogram.dispatcher.dispatcher import FSMContextMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup

ID = None

TOKEN = config("TOKEN")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config("TOKEN"))
dp = Dispatcher()


class FSMAdmin(StatesGroup):
    admin_request = State()
    new_value = State()


@dp.message(commands=["moderator"], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Ready for work')
    await message.delete()


@dp.message(commands=["Change"], state=None)
async def cm_start(message: types.Message):
    await FSMAdmin.admin_request.set()
    await message.reply('enter the variable to be changed')


@dp.message(content_types=["admin_request"], state=FSMAdmin.admin_request)
async def load_photo(message: types.Message, state: FSMContextMiddleware):
    async with state.proxy() as data:
        data["admin_request"] = message.admin_request[0].file_id
    await FSMAdmin.next()
    await message.reply("enter new value")




