import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from decouple import config
from aiogram.utils.keyboard import InlineKeyboardBuilder
import aioschedule
import sqlite3
from datetime import datetime, timedelta



TOKEN = config("TOKEN")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

conn = sqlite3.connect('db_aiogram_tg.db', check_same_thread=False)
cursor = conn.cursor()
time1 = None


async def check_for_changes():
    async def get_reminders():
        but1 = cursor.execute(f"SELECT name FROM buttons WHERE buttom = 'reminder_button'")
        but1 = cursor.fetchone()
        but11 = cursor.execute(f"SELECT url FROM buttons WHERE buttom = 'reminder_button'")
        but11 = cursor.fetchone()
        builder = InlineKeyboardBuilder()
        if but1[0] != """off""":
            builder.row(types.InlineKeyboardButton(
                text=but1[0],
                url=but11[0]))

        notification1 = cursor.execute(f"SELECT time, text FROM table_info WHERE name = 'notification'")
        notification1 = cursor.fetchone()
        await bot.send_message(chat_id=config("chat_id"),
                               text=f"""{notification1[1]}""",
                               reply_markup=builder.as_markup())

    time_new = cursor.execute(f"SELECT new FROM reminders WHERE name = 'reminder'")
    time_new = cursor.fetchone()
    time_old = cursor.execute(f"SELECT old FROM reminders WHERE name = 'reminder'")
    time_old = cursor.fetchone()
    if time_new[0] == 0:
        cursor.execute(fr"""UPDATE reminders SET old = {time_new[0]} WHERE name = "reminder" """)
        conn.commit()
        pass
    else:
        if time_new[0] != time_old[0]:
            cursor.execute(fr"""UPDATE reminders SET old = {time_new[0]} WHERE name = "reminder" """)
            conn.commit()
            datetime_write = datetime.now() + timedelta(hours=time_new[0])
            str_dt_write = datetime_write.strftime('%d.%m.%Y %H:%M:%S')
            cursor.execute(fr"""UPDATE reminders SET date = "{str_dt_write}" WHERE name = "reminder" """)
            conn.commit()
        elif time_new[0] == time_old[0]:
            time_reminder = cursor.execute(f"""SELECT date FROM reminders WHERE name = "reminder" """)
            time_reminder = cursor.fetchone()
            time_remind = datetime.strptime(time_reminder[0], '%d.%m.%Y %H:%M:%S')
            if datetime.now().strftime('%d.%m.%Y %H:%M') == time_remind.strftime('%d.%m.%Y %H:%M'):
                new_date = time_remind + timedelta(hours=time_new[0])
                new_date = new_date.strftime('%d.%m.%Y %H:%M:%S')
                cursor.execute(fr"""UPDATE reminders SET date = "{new_date}" WHERE name = "reminder" """)
                conn.commit()

                await get_reminders()


async def main():
    aioschedule.every(1).minutes.do(check_for_changes)

    while True:
        try:
            await aioschedule.run_pending()
        except:
            pass





































if __name__ == "__main__":
    asyncio.run(main())
