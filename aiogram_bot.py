import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from decouple import config
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


TOKEN = config("TOKEN")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def on_user_joined(message: types.Message):

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Cryptostorm.net",
        url="cryptostorm.net"))
    builder.row(types.InlineKeyboardButton(
        text="Official support agent",
        url="https://t.me/SIBWalletBot"))

    await message.delete()
    for user in message.new_chat_members:
        await message.answer(f"""<b>{user.first_name}</b>, Welcome to cryptostorm.net official support channel!

The only official support agent is @cryptosupport

Our staff will never PM you first, ask for any sensitive information or request a fund transfer. """,
                             reply_markup=builder.as_markup(),
                             parse_mode="HTML"
                             )


@dp.message(content_types=["text"])
async def message_filter(message: types.Message):

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Official support agent",
        url="https://t.me/SIBWalletBot"))

    data = {
        "url": ",N/A",
        "email": "N/A"
    }

    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            await message.delete()
            await message.answer(
                "Dear Customer, please don't send your personal info to public chat! If you have any questions, please text private message to our support team @cryptosupport",
            reply_markup=builder.as_markup())



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
