import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from decouple import config
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

TOKEN = config("TOKEN")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config("TOKEN"))
dp = Dispatcher()


@dp.message(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def on_user_joined(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text=config("welcome_text1"),
        url=config("welcome_url1")))
    builder.row(types.InlineKeyboardButton(
        text=config("welcome_text2"),
        url=config("welcome_url2")))
    builder.row(types.InlineKeyboardButton(
        text=config("welcome_text3"),
        url=config("welcome_url3")))

    await message.delete()
    for user in message.new_chat_members:
        await message.answer(f"""<b>{user.first_name}</b>, {config('welcome_message')}""",
                             reply_markup=builder.as_markup(),
                             parse_mode="HTML"
                             )


@dp.message(content_types=["text"])
async def message_filter(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text=config("warning_text"),
        url=config("warning_url")))

    data = {
        "url": ",N/A",
        "email": "N/A"
    }

    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            await message.delete()
            await message.answer(config("warning_message"),
                                 reply_markup=builder.as_markup())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
