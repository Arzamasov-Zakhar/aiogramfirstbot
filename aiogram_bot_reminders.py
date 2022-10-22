import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from decouple import config
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import aioschedule


TOKEN = config("TOKEN")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

time1 = 1


async def reminder():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text=config("reminder_text"),
        url=config("reminder_text")))

    await bot.send_message(chat_id=config("chat_id"),
                           text=f"""Dear Customers, beware of fraudsters! 
Our team will never message you first or request a fund transfer anywhere except the {config("reminder_message1")} website. There is no “manual mode” for transactions, everything goes through the website!""",
                           reply_markup=builder.as_markup())


async def main():
    aioschedule.every(time1).hours.do(reminder)

    while True:
        await aioschedule.run_pending()


if __name__ == "__main__":
    asyncio.run(main())
