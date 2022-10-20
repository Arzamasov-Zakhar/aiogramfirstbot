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
        text="itez.com",
        url=" itez.com"))

    await bot.send_message(chat_id="-872126641",
        text="""Dear Customers, beware of fraudsters!
Our team will never message you first or request a fund transfer anywhere except the itez.com website. There is no “manual mode” for transactions, everything goes through the website!""",

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
