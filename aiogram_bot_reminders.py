import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from decouple import config
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

TOKEN = config("TOKEN")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message()
async def reminder():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text=config("reminder_text"),
        url=config("reminder_text")))

    await bot.send_message(chat_id=config("chat_id"),
                           text=config("reminder_message"),
                           reply_markup=builder.as_markup())


async def working():
    while True:
        await reminder()
        await asyncio.sleep(15)


async def main():
    await dp.start_polling(bot, on_startup=working)


if __name__ == "__main__":
    asyncio.run(main())

# async def periodic(sleep_for):
#     while True:
#         await asyncio.sleep(sleep_for)
#         await reminder()
#         await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     dp.
#     dp.loop.create_task(periodic(10))
#     await dp.start_polling(bot)
# async def main():
#     await reminder()
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
