import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from decouple import config
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import html
import string
import sqlite3
from sqlite3 import IntegrityError
from datetime import datetime

ID = None

while True:
    try:

        TOKEN = config("TOKEN")
        logging.basicConfig(level=logging.INFO)
        bot = Bot(token=config("TOKEN"))
        dp = Dispatcher()

        conn = sqlite3.connect('db_aiogram_tg.db', check_same_thread=False)
        cursor = conn.cursor()


        @dp.message(commands=["admin"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                if len(message.text.split()) > 1:
                    text1 = message.text.split(' ', 1)[1]
                    wordpass = cursor.execute(f"SELECT name FROM other_things WHERE other = 'wordpass'")
                    wordpass = cursor.fetchone()
                    if text1 == wordpass[0]:
                        admin_id1 = message.from_user.id
                        try:
                            cursor.execute(f"""INSERT INTO id_list VALUES (?)""", (f'{admin_id1}',))
                            conn.commit()
                            await message.answer('Слушаю.')
                        except IntegrityError:
                            await message.answer('Вы не выходили из учетной записи.')


        @dp.message(commands=["logout"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                leave_id = message.from_user.id
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if leave_id in id_list:
                    await message.answer('Good bye!')
                    cursor.execute(f"""DELETE FROM id_list WHERE id='{message.from_user.id}' """)
                    conn.commit()


        @dp.message(commands=["start"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
            if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                await message.answer('введите /help, чтобы получить всю необходимую информацию')
                cursor.execute('''CREATE TABLE IF NOT EXISTS table_info (
                                name STRING UNIQUE,
                                time INTEGER,
                                text TEXT
                                )''')
                conn.commit()
                cursor.execute('''CREATE TABLE IF NOT EXISTS ban_list (
                                        bad_word INTEGER UNIQUE)''')
                conn.commit()

                cursor.execute('''CREATE TABLE IF NOT EXISTS id_list (
                                                id INTEGER UNIQUE)''')
                conn.commit()

                cursor.execute('''CREATE TABLE IF NOT EXISTS buttons (
                                buttom STRING UNIQUE,
                                name TEXT,
                                url TEXT
                                )''')
                conn.commit()
                cursor.execute('''CREATE TABLE IF NOT EXISTS other_things (
                                        other STRING UNIQUE,
                                        name TEXT
                                        )''')
                conn.commit()

                cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (
                                                name STRING UNIQUE,
                                                old INTEGER,
                                                new INTEGER,
                                                date TEXT
                                                )''')
                conn.commit()

                try:
                    cursor.execute(f'INSERT or IGNORE INTO table_info VALUES (?, ?, ?)',
                                   ('TEXT', 6, f"""TEXT"""))
                    cursor.execute(f'INSERT or IGNORE INTO table_info VALUES (?, ?, ?)',
                                   ('TEXT', None, f""", TEXT"""))
                    cursor.execute(f'INSERT or IGNORE INTO buttons VALUES (?, ?, ?)',
                                   ('welcome_button1', 'TEXT', 'TEXT'))
                    cursor.execute(f'INSERT or IGNORE INTO buttons VALUES (?, ?, ?)',
                                   ('welcome_button2', 'TEXT', 'TEXT'))
                    cursor.execute(f'INSERT or IGNORE INTO buttons VALUES (?, ?, ?)',
                                   ('welcome_button3', 'TEXT', 'TEXT'))
                    cursor.execute(f'INSERT or IGNORE INTO buttons VALUES (?, ?, ?)',
                                   ('warning_button', 'TEXT', 'TEXT'))
                    cursor.execute(f'INSERT or IGNORE INTO buttons VALUES (?, ?, ?)',
                                   ('reminder_button', 'TEXT', 'TEXT'))
                    conn.commit()
                    cursor.execute(f'INSERT or IGNORE INTO other_things VALUES (?, ?)',
                                   ('TEXT', 'TEXT'))
                    conn.commit()
                    dt_now = datetime.now()
                    str_dt_now = dt_now.strftime('%d.%m.%Y %H:%M:%S')
                    cursor.execute(f'INSERT or IGNORE INTO reminders VALUES (?, ?, ?, ?)',
                                   ('reminder', 6, 6, f"""{str_dt_now}"""))
                    conn.commit()


                except IntegrityError:
                    pass


        @dp.message(commands=["help"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
            if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                await message.answer(r"""
/info информация
/change_reminder_time "целое число часов"  -  Изменить таймер рассылки.
Внимание: для отключения рассылки поставьте цифру 0.
/change_reminder_text "Новый текст рассылки"  - Изменить текст рассылки.

/change_welcome_text "Новый текст приветствия"  - Изменить текст приветствия.

/change_warning_text "Новый текст предупреждения"  - Изменить текст предупреждения.

/add_word "Слово" - Добавить слово в бан-лист.
/delete_word "Слово" - Удалить слово из бан-листа.


/change_warning_button_name "Новое название кнопки" - Изменить название кнопки предупреждения.
/change_warning_button_url "Новый url кнопки" - Изменить url кнопки предупреждения.
/change_reminder_button_name "Новое название кнопки" - Изменить название кнопки рассылки.
/change_reminder_button_url "Новый url кнопки"  - Изменить url кнопки рассылки.
/change_welcome_button1_name "Новое название кнопки" - Изменить название кнопки1 приветствия.
/change_welcome_button1_url "Новый url кнопки" - Изменить url кнопки1 приветствия.
/change_welcome_button2_name "Новое название кнопки" - Изменить название кнопки2 приветствия.
/change_welcome_button2_url "Новый url кнопки" - Изменить url кнопки2 приветствия.
/change_welcome_button3_name "Новое название кнопки" - Изменить название кнопки3 приветствия.
/change_welcome_button3_url "Новый url кнопки" - Изменить url кнопки3 приветствия.
ВНИМАНИЕ: для удаления кнопки, измените название кнопки на off .


/reset - Откатить до начальных настроек.
/admin - Открыть админ-сессию(также, в группе не будут фильтроваться сообщения от Вас).
/logout - Закрыть админ-сессию(также, в группе будут фильтроваться сообщения от Вас).
/info_admins - Показать ID активных админов.
/another_password "Новый пароль" - Изменить пароль.
/actual_password - Показать пароль.
"""
                                     )


        @dp.message(commands=["info"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    notification1 = cursor.execute(f"SELECT time, text FROM table_info WHERE name = 'notification'")
                    notification1 = cursor.fetchone()
                    welcome1 = cursor.execute(f"SELECT text FROM table_info WHERE name = 'welcome'")
                    welcome1 = cursor.fetchone()
                    warning1 = cursor.execute(f"SELECT text FROM table_info WHERE name = 'warning'")
                    warning1 = cursor.fetchone()
                    ban_list1 = cursor.execute(f"SELECT bad_word FROM ban_list ")

                    ban_list = []
                    for i in ban_list1:
                        ban_list.append(i[0])

                    await message.answer(f"""
Время рассылки в часах:   {notification1[0]}.

Текст рассылки: 
{notification1[1]}
--------------------
Текст приветствия: 
"User_name"{welcome1[0]}
--------------------
Текст предупреждения: 
{warning1[0]}
--------------------
Бан-лист: {'; '.join(ban_list)}
"""
                                         )


        @dp.message(commands=["change_reminder_time"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_time введите целое число.")
                    else:
                        try:
                            time1 = int(message.text.split()[1])
                            if 0 <= time1:
                                cursor.execute(fr"""UPDATE table_info SET time = {time1} WHERE name = "notification" """)
                                conn.commit()
                                cursor.execute(fr"""UPDATE reminders SET new = {time1} WHERE name = "reminder" """)
                                conn.commit()
                                if time1 > 0:
                                    await message.answer(f"Интервал рассылки изменен, новый интервал в часах: {time1}")
                                else:
                                    await message.answer(f"Рассылка отключена.")
                            else:
                                await message.answer(r"Пожалуйста, после команды /change_time введите целое число не меньше 0.")
                        except ValueError:
                            await message.answer(r"Пожалуйста, после команды /change_time введите целое число.")


        @dp.message(commands=["change_reminder_text"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_time_text введите текст рассылки.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        await message.answer(f"Текст рассылки изменен, новый текст рассылки: {text1}")
                        cursor.execute(fr"""UPDATE table_info SET text = "{text1}" WHERE name = "notification" """)
                        conn.commit()


        @dp.message(commands=["change_welcome_text"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_welcome_text введите текст приветствия.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        await message.answer(f"Текст приветствия изменен, новый текст приветствия: {text1}")
                        cursor.execute(fr"""UPDATE table_info SET text = "{text1}" WHERE name = "welcome" """)
                        conn.commit()


        @dp.message(commands=["change_warning_text"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_warning_text введите текст предупреждения.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        await message.answer(f"Текст предупреждения изменен, новый текст предупреждения: {text1}")
                        cursor.execute(fr"""UPDATE table_info SET text = "{text1}" WHERE name = "warning" """)
                        conn.commit()


        @dp.message(commands=["change_warning_button_name"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_warning_button_name введите текст кнопки.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        if text1 == "off":
                            await message.answer(f"Кнопка отключена, для включения - переименуйте кнопку в необходимое Вам название.")
                            cursor.execute(fr"""UPDATE buttons SET name = "{text1}" WHERE buttom = "warning_button" """)
                            conn.commit()
                        else:
                            await message.answer(f"Текст кнопки изменен, новый текст кнопки: {text1}")
                            cursor.execute(fr"""UPDATE buttons SET name = "{text1}" WHERE buttom = "warning_button" """)
                            conn.commit()


        @dp.message(commands=["change_warning_button_url"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_warning_button_url введите url кнопки.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        await message.answer(f"Url кнопки изменен, новый url кнопки: {text1}")
                        cursor.execute(fr"""UPDATE buttons SET url = "{text1}" WHERE buttom = "warning_button" """)
                        conn.commit()


        @dp.message(commands=["change_reminder_button_name"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_reminder_button_name введите текст кнопки.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        if text1 == "off":
                            await message.answer(f"Кнопка отключена, для включения - переименуйте кнопку в необходимое Вам название.")
                            cursor.execute(fr"""UPDATE buttons SET name = "{text1}" WHERE buttom = "reminder_button" """)
                            conn.commit()
                        else:
                            await message.answer(f"Текст кнопки изменен, новый текст кнопки: {text1}")
                            cursor.execute(fr"""UPDATE buttons SET name = "{text1}" WHERE buttom = "reminder_button" """)
                            conn.commit()


        @dp.message(commands=["change_reminder_button_url"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_reminder_button_url введите url кнопки.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        await message.answer(f"Url кнопки изменен, новый url кнопки: {text1}")
                        cursor.execute(fr"""UPDATE buttons SET url = "{text1}" WHERE buttom = "reminder_button" """)
                        conn.commit()


        @dp.message(commands=["change_welcome_button1_name"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_welcome_button1_name введите текст кнопки.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        if text1 == "off":
                            await message.answer(f"Кнопка отключена, для включения - переименуйте кнопку в необходимое Вам название.")
                            cursor.execute(fr"""UPDATE buttons SET name = "{text1}" WHERE buttom = "welcome_button1" """)
                            conn.commit()
                        else:
                            await message.answer(f"Текст кнопки изменен, новый текст кнопки: {text1}")
                            cursor.execute(fr"""UPDATE buttons SET name = "{text1}" WHERE buttom = "welcome_button1" """)
                            conn.commit()


        @dp.message(commands=["change_welcome_button1_url"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_welcome_button1_url введите url кнопки.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        await message.answer(f"Url кнопки изменен, новый url кнопки: {text1}")
                        cursor.execute(fr"""UPDATE buttons SET url = "{text1}" WHERE buttom = "welcome_button1" """)
                        conn.commit()


        @dp.message(commands=["change_welcome_button2_name"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_welcome_button2_name введите текст кнопки.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        if text1 == "off":
                            await message.answer(f"Кнопка отключена, для включения - переименуйте кнопку в необходимое Вам название.")
                            cursor.execute(fr"""UPDATE buttons SET name = "{text1}" WHERE buttom = "welcome_button2" """)
                            conn.commit()
                        else:
                            await message.answer(f"Текст кнопки изменен, новый текст кнопки: {text1}")
                            cursor.execute(fr"""UPDATE buttons SET name = "{text1}" WHERE buttom = "welcome_button2" """)
                            conn.commit()


        @dp.message(commands=["change_welcome_button2_url"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_welcome_button2_url введите url кнопки.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        await message.answer(f"Url кнопки изменен, новый url кнопки: {text1}")
                        cursor.execute(fr"""UPDATE buttons SET url = "{text1}" WHERE buttom = "welcome_button2" """)
                        conn.commit()


        @dp.message(commands=["change_welcome_button3_name"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_welcome_button3_name введите текст кнопки.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        if text1 == "off":
                            await message.answer(f"Кнопка отключена, для включения - переименуйте кнопку в необходимое Вам название.")
                            cursor.execute(fr"""UPDATE buttons SET name = "{text1}" WHERE buttom = "welcome_button3" """)
                        else:
                            await message.answer(f"Текст кнопки изменен, новый текст кнопки: {text1}")
                            cursor.execute(fr"""UPDATE buttons SET name = "{text1}" WHERE buttom = "welcome_button3" """)
                            conn.commit()


        @dp.message(commands=["change_welcome_button3_url"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /change_welcome_button3_url введите url кнопки.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        await message.answer(f"Url кнопки изменен, новый url кнопки: {text1}")
                        cursor.execute(fr"""UPDATE buttons SET url = "{text1}" WHERE buttom = "welcome_button3" """)
                        conn.commit()


        @dp.message(commands=["add_word"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /add_word введите 1 слово.")
                    else:
                        text1 = message.text.split(' ')[1].lower()
                        await message.answer(fr"""В бан-лист добавлено слово: {text1}""")
                        cursor.execute(f"""INSERT INTO ban_list VALUES (?)""", (f'{text1}',))
                        conn.commit()


        @dp.message(commands=["delete_word"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /delete_word введите 1 слово.")
                    else:
                        text1 = message.text.split(' ')[1]
                        await message.answer(fr"Из бан-листа удалено слово: {text1}")
                        cursor.execute(f"""DELETE FROM ban_list WHERE bad_word='{text1}' """)
                        conn.commit()


        @dp.message(commands=["reset"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    try:
                        time1 = 6
                        text1 = f"""TEXT"""
                        text2 = f"""TEXT"""
                        text3 = """TEXT"""
                        cursor.execute(fr"""UPDATE table_info SET time = {time1} WHERE name = "notification" """)
                        cursor.execute(fr"""UPDATE reminders SET new = {time1} WHERE name = "reminder" """)
                        cursor.execute(fr"""UPDATE table_info SET text = "{text1}" WHERE name = "notification" """)
                        cursor.execute(fr"""UPDATE table_info SET text = "{text2}" WHERE name = "welcome" """)
                        cursor.execute(fr"""UPDATE table_info SET text = "{text3}" WHERE name = "warning" """)
                        conn.commit()
                        await message.answer(fr"Сброшено до начальных настроек. Введите /info для информации.")
                    except IntegrityError:
                        pass


        @dp.message(commands=["another_password"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    if len(message.text.split()) == 1:
                        await message.answer(r"Пожалуйста, после команды /another_password введите новый пароль.")
                    else:
                        text1 = message.text.split(' ', 1)[1]
                        await message.answer(f"Пароль изменен, новый пароль: {text1}")
                        cursor.execute(fr"""UPDATE other_things SET name = "{text1}" WHERE other = "wordpass" """)
                        conn.commit()


        @dp.message(commands=["info_admins"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    admin_list1 = cursor.execute(f"SELECT id FROM id_list ")
                    admin_list = []
                    for i in admin_list1:
                        admin_list.append(str(i[0]))

                    await message.answer(f"""Список ID активных админов:
        {'; '.join(admin_list)}
        Полную инфомацию о пользователе можно узнать, написав его ID данному боту @usinfobot.""")


        @dp.message(commands=["actual_password"])
        async def info(message: types.Message):
            if message.chat.id != int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id == int(config("admin_id")) or message.from_user.id in id_list:
                    wordpass = cursor.execute(f"""SELECT name FROM other_things WHERE other="wordpass" """)
                    wordpass = cursor.fetchone()
                    await message.answer(f"""{wordpass[0]}""")


        @dp.message(content_types=types.ContentType.NEW_CHAT_MEMBERS)
        async def on_user_joined(message: types.Message):
            if message.chat.id == int(config("chat_id")):
                butt1 = cursor.execute(f"SELECT name FROM buttons WHERE buttom = 'welcome_button1'")
                butt1 = cursor.fetchone()
                butt11 = cursor.execute(f"SELECT url FROM buttons WHERE buttom = 'welcome_button1'")
                butt11 = cursor.fetchone()
                butt2 = cursor.execute(f"SELECT name FROM buttons WHERE buttom = 'welcome_button2'")
                butt2 = cursor.fetchone()
                butt22 = cursor.execute(f"SELECT url FROM buttons WHERE buttom = 'welcome_button2'")
                butt22 = cursor.fetchone()
                butt3 = cursor.execute(f"SELECT name FROM buttons WHERE buttom = 'welcome_button3'")
                butt3 = cursor.fetchone()
                butt33 = cursor.execute(f"SELECT url FROM buttons WHERE buttom = 'welcome_button3'")
                butt33 = cursor.fetchone()

                builder = InlineKeyboardBuilder()
                if butt1[0] != """off""":
                    builder.row(types.InlineKeyboardButton(
                        text=butt1[0],
                        url=butt11[0]))
                if butt2[0] != """off""":
                    builder.row(types.InlineKeyboardButton(
                        text=butt2[0],
                        url=butt22[0]))
                if butt3[0] != """off""":
                    builder.row(types.InlineKeyboardButton(
                        text=butt3[0],
                        url=butt33[0]))

                await message.delete()
                for user in message.new_chat_members:
                    welcome1 = cursor.execute(f"SELECT text FROM table_info WHERE name = 'welcome'")
                    welcome1 = cursor.fetchone()
                    await message.answer(
                        f"""<b>{html.bold(html.quote(user.first_name))}</b>{welcome1[0]}""",
                        reply_markup=builder.as_markup(),
                        parse_mode="HTML"
                    )


        @dp.message(content_types=types.ContentType.LEFT_CHAT_MEMBER)
        async def on_user_left(message: types.Message):
            if message.chat.id == int(config("chat_id")):
                await message.delete()


        @dp.message(content_types=["text"])
        async def message_filter(message: types.Message):
            if message.chat.id == int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id != int(config("admin_id")) and message.from_user.id not in id_list:
                    but1 = cursor.execute(f"SELECT name FROM buttons WHERE buttom = 'warning_button'")
                    but1 = cursor.fetchone()
                    but11 = cursor.execute(f"SELECT url FROM buttons WHERE buttom = 'warning_button'")
                    but11 = cursor.fetchone()
                    builder = InlineKeyboardBuilder()
                    if but1[0] != """off""":
                        builder.row(types.InlineKeyboardButton(
                            text=but1[0],
                            url=but11[0]))

                    data = {
                        "url": ",N/A",
                        "email": "N/A"
                    }

                    entities = message.entities or []
                    for item in entities:
                        if item.type in data.keys():
                            await message.delete()
                            warning1 = cursor.execute(f"SELECT text FROM table_info WHERE name = 'warning'")
                            warning1 = cursor.fetchone()
                            await message.answer(
                                warning1[0],
                                reply_markup=builder.as_markup())
                            return None

                mat_list = ['6ля', '6лядь', '6лять', 'b3ъeб', 'cock', 'cunt', 'e6aль', 'ebal', 'eblan', 'e6 ', 'eб ', 'eбaл',
                            'eбaть', 'eбyч', 'eбать', 'eблантий', 'eбёт', 'fuck', 'fucker', 'fucking', 'xyй', 'xyя', 'xyёв',
                            'xуе', 'xуй', 'xую', 'zaeb', 'zaebal', 'zaebali', 'zaebat', 'Нехуй', 'архипиздрит', 'ахуел',
                            'ахуеть', 'бздение', 'бздеть', 'бздех', 'бздецы', 'бздит', 'бздицы', 'бздло', 'бзднуть', 'бздун',
                            'бздунья', 'бздюха', 'бздюшка', 'бздюшко', 'бля', 'блябу', 'блябуду', 'бляд', 'бляди', 'блядина',
                            'блядище', 'блядки', 'блядовать',
                            'блядство', 'блядун', 'блядуны', 'блядунья', 'блядь', 'блядюга', 'блять', 'вафел', 'вафлёр',
                            'взъебка',
                            'взьебка', 'взьебывать', 'въеб', 'въебался', 'въебенн', 'въебусь', 'въебывать', 'выблядок',
                            'выблядыш',
                            'выеб', 'выебать', 'выебен', 'выебнулся', 'выебон', 'выебываться', 'выпердеть', 'высраться',
                            'выссаться',
                            'вьебен', 'гавно', 'гавнюк', 'гавнючка', 'гамно', 'гандон', 'гнид', 'гнида', 'гниды', 'говенка',
                            'говенный',
                            'говешка', 'говназия', 'говнецо', 'говнище', 'говно', 'говноед', 'говнолинк', 'говночист', 'говнюк',
                            'говнюха', 'говнядина', 'говняк', 'говняный', 'говнять', 'гондон', 'доебываться', 'долбоеб',
                            'долбоящер',
                            'долбоёб', 'дрисня', 'дрист', 'дристануть', 'дристать', 'дристун', 'дристуха', 'дрочелло',
                            'дрочена',
                            'дрочила', 'дрочилка', 'дрочистый', 'дрочить', 'дрочка', 'дрочун', 'е6ал', 'е6ут', ' еб ', ' ёб ',
                            'ебaть',
                            'ебyч', 'ебал', 'ебало', 'ебальник', 'ебан', 'ебанамать', 'ебанат', 'ебаная', 'ебанический',
                            'ебанный',
                            'ебанныйврот', 'ебаное', 'ебануть', 'ебануться', 'ебаный', 'ебанько', 'ебарь', 'ебат', 'ебатория',
                            'ебать',
                            'ебать-копать', 'ебаться', 'ебашить', 'ебет', 'ебет', 'ебец', 'ебик', 'ебин', 'ебись', 'ебическая',
                            'ебки',
                            'ебла', 'еблан', 'ебливый', 'еблище', 'ебло', 'еблыст', 'ебля', 'ебнуть', 'ебнуться', 'ебня',
                            'ебошить',
                            'ебская', 'ебский', 'ебтвоюмать', 'ебун', 'ебут', 'ебуч', 'ебуче', 'ебучее', 'ебучий', 'ебучим',
                            'ебущ',
                            'ебырь', 'ебёна', 'ебёт', 'ебёт', 'елда', 'елдак', 'елдачить', 'жопа', 'жопу', 'заговнять',
                            'задрачивать',
                            'задристать', 'задрота', 'зае6', 'заеб', 'заеба', 'заебал', 'заебанец', 'заебастая', 'заебастый',
                            'заебать',
                            'заебаться', 'заебашить', 'заебистое', 'заебистые', 'заебистый', 'заебись', 'заебошить',
                            'заебываться',
                            'залуп', 'залупа', 'залупаться', 'залупить', 'залупиться', 'замудохаться', 'запиздячить',
                            'засерать',
                            'засерун', 'засеря', 'засирать', 'засрун', 'захуячить', 'заябестая', 'заё6', 'заёб', 'заёбистое',
                            'заёбистые', 'заёбистый', 'злоеб', 'злоебучая', 'злоебучее', 'злоебучий', 'ибанамат', 'ибонех',
                            'изговнять',
                            'изговняться', 'изъебнуться', 'ипать', 'ипаться', 'ипаццо', 'конча', 'курва', 'курвятник', 'лох',
                            'лошарa',
                            'лошара', 'лошары', 'лошок', 'лярва', 'малафья', 'манда', 'мандавошек', 'мандавошка', 'мандавошки',
                            'мандей', 'мандень', 'мандеть', 'мандища', 'мандой', 'манду', 'мандюк', 'минет', 'минетчик',
                            'минетчица', 'млять', 'мокрощелка', 'мокрощёлка', 'мразь', 'мудak', 'мудaк', 'мудаг', 'мудак',
                            'муде',
                            'мудель', 'мудеть', 'муди', 'мудил', 'мудила', 'мудистый', 'мудня', 'мудоеб', 'мудозвон',
                            'мудоклюй', 'набздел', 'набздеть', 'наговнять', 'надристать', 'надрочить', 'наебать', 'наебет',
                            'наебнуть',
                            'наебнуться', 'наебывать', 'напиздел', 'напиздели', 'напиздело', 'напиздили', 'насрать',
                            'настопиздить',
                            'нахер', 'нахрен', 'нахуй', 'нахуйник', 'невротебучий', 'невъебенно', 'нехира',
                            'нехрен',
                            'нехуйственно', 'ниибацо', 'ниипацца', 'ниипаццо', 'ниипет', 'никуя', 'нихера', 'нихуя',
                            'обдристаться',
                            'обосранец', 'обосрать', 'обосцать', 'обосцаться', 'обсирать', 'объебос', 'обьебать', 'обьебос',
                            'однохуйственно', 'опездал', 'опизде', 'опизденивающе', 'остоебенить', 'остопиздеть', 'отмудохать',
                            'отпиздить', 'отпиздячить', 'отпороть', 'отъебись', 'охуевательский', 'охуевать', 'охуевающий',
                            'охуел',
                            'охуенно', 'охуеньчик', 'охуеть', 'охуительно', 'охуительный', 'охуяньчик', 'охуячивать',
                            'охуячить',
                            'очкун', 'падла', 'падонки', 'падонок', 'паскуда', 'педерас', 'педик', 'педрик', 'педрила',
                            'педрилло',
                            'педрило', 'педрилы', 'пездень', 'пездит', 'пездишь', 'пездо', 'пездят', 'пердануть', 'пердеж',
                            'пердение',
                            'пердеть', 'пердильник', 'перднуть', 'пердун', 'пердунец', 'пердунина', 'пердунья', 'пердуха',
                            'пердь',
                            'переёбок', 'пернуть', 'пи3д', 'пи3де', 'пи3ду', 'пиzдец', 'пидар', 'пидарaс', 'пидарас',
                            'пидарасы',
                            'пидары', 'пидор', 'пидорасы', 'пидорка', 'пидорок', 'пидоры', 'пидрас', 'пизда', 'пиздануть',
                            'пиздануться', 'пиздарваньчик', 'пиздато', 'пиздатое', 'пиздатый', 'пизденка', 'пизденыш',
                            'пиздеть',
                            'пиздец', 'пиздит', 'пиздить', 'пиздиться', 'пиздишь', 'пиздища', 'пиздище', 'пиздобол',
                            'пиздоболы',
                            'пиздобратия', 'пиздоватая', 'пиздоватый', 'пиздолиз', 'пиздонутые', 'пиздорванец', 'пиздорванка',
                            'пиздострадатель', 'пизду', 'пиздуй', 'пиздун', 'пиздунья', 'пизды', 'пиздюга', 'пиздюк',
                            'пиздюлина', 'пиздa', 'пи3дa', 'пездa', 'пе3дa', 'пe3дa', 'пeзда', 'пе3да', 'пeзда',
                            'пиздюля', 'пиздят', 'пиздячить', 'пиздёныш', 'писбшки', 'писька', 'писькострадатель', 'писюн',
                            'писюшка', 'подговнять', 'подонки', 'подонок', 'подъебнуть', 'подъебнуться', 'поебать', 'поебень',
                            'поскуда', 'посрать', 'потаскуха', 'потаскушка', 'похер', 'похерил', 'похерила', 'похерили',
                            'похеру',
                            'похрен', 'похрену', 'похуист', 'похуистка', 'похуй', 'похую', 'поёбываает', 'придурок',
                            'приебаться',
                            'припиздень', 'припизднутый', 'припиздюлина', 'пробзделся', 'проблядь', 'проеб', 'проебанка',
                            'проебать',
                            'промандеть', 'промудеть', 'пропизделся', 'пропиздеть', 'пропиздячить', 'пёрднуть', 'пёрнуть',
                            'раздолбай',
                            'разхуячить', 'разъеб', 'разъеба', 'разъебай', 'разъебать', 'распиздай', 'распиздеться',
                            'распиздяй',
                            'распиздяйство', 'сволота', 'сволочь', 'сговнять', 'секель', 'серун', 'серька', 'сестроеб',
                            'сикель', 'сирать', 'сирывать', 'соси', 'спездел', 'спездеть', 'спездил', 'спездила',
                            'спездили', 'спездит', 'спездить', 'спездел', 'спиздеть', 'спиздил', 'спиздила',
                            'спиздили', 'спиздит', 'спиздить', 'cпиздел', 'cпиздеть', 'cпиздил', 'cпиздила',
                            'спиздили', 'спиздит', 'спиздить', 'срака', 'сраку', 'сраный', 'сранье', 'срать', 'срун', 'ссака',
                            'ссышь', 'стерва', 'страхопиздище', 'сука', 'суки', 'суходрочка', 'сучара', 'сучий', 'сучка',
                            'сучко', 'сучонок', 'сучье',
                            'сцание', 'сцать', 'сцука', 'сцуки', 'сцуконах', 'сцуль', 'сцыха', 'сцышь', 'съебаться', 'сыкун',
                            'трахае6', 'трахаеб', 'трахатель', 'трахаёб', 'ублюдок', 'уебать', 'уебище', 'уебищное',
                            'уебк',
                            'уебки', 'уебок', 'усраться', 'ушлепок', 'уёбища', 'уёбище', 'уёбищное', 'уёбки', 'уёбок',
                            'х_у_я_р_а', 'хyй', 'хyйня', 'хyё', 'хамло', 'хер', 'хер', 'херня', 'херовато', 'херовина',
                            'херовый',
                            'хитровыебанный', 'хитрожопый', 'хуeм', 'хуе', 'хуевато', 'хуевина', 'хуево', 'хуевый', 'хуек',
                            'хуел',
                            'хуем', 'хуенч', 'хуеныш', 'хуенький', 'хуеплет', 'хуеплёт', 'хуепромышленник', 'хуерик', 'хуерыло',
                            'хуесос', 'хуесоска', 'хуета', 'хуетень', 'хуею', 'хуи', 'хуище', 'хуй', 'хуй', 'хуй', 'хуйком',
                            'хуйло',
                            'хуйня', 'хуйрик', 'хуля', 'хую', 'хую', 'хуюл', 'хуя', 'хуяк', 'хуякать', 'хуякнуть', 'хуяра',
                            'хуясе',
                            'хуячить', 'хуё', 'хуёвенький', 'хуёвый', 'хуёк', 'целка', 'чмо', 'чмошник', 'чмырь', 'шалава',
                            'шалавой',
                            'шараёбиться', 'шлюха', 'шлюхой', 'шлюшка', 'ябывает', 'ёб', 'ёбaн', 'ёбаная', 'ёбаную', 'ёбат',
                            'ёбн', "пидoр", 'пидоp', 'пидop', 'пидap', 'пидap', 'пидap',
                            "хуй", "пизд", "гондо", "пидор", "педи", "педо", "педа", "чмо", "говн", "шлюх", "шлюш", "хуя",
                            "хуе", "хуи",
                            "лох", "соса", "сука", "сучка", "сучок", "сучек", "суча", "гандо", "ган", "ибл", "ебл", "ёбл",
                            "еба", "ибу",
                            "иба", "нахе", "наху", "неху", "fuck", "shit", "crap ", "damn", "nigg", "niga", "bitch", "whore",
                            "slut",
                            "freak", "gay", "faggot", "bastard", "homo", "asshole", "noob", "dick", "suck", "jerk", "hooker",
                            "ass",
                            "cunt", "twat", "йух", "адзип", "нодног", "ноднаг", "родип", "онвог", "онваг", "омч", "kcuf",
                            "hctib",
                            "kcid", "kcus", "tnuc", "яух", "писю", "писос", "писд", "писка", "письк", "песю", "шалав", "хули",
                            "йуx", "йyх", "йyx", "пиcда", "пи3дa", "пиздa"]

                ban_list1 = cursor.execute(f"SELECT bad_word FROM ban_list ")
                ban_list: list = []
                for i in ban_list1:
                    ban_list.append(i[0])

                if {i.translate(str.maketrans('', '', string.punctuation)) for i in message.text.lower().split(' ')} \
                        .intersection(set(mat_list)) or {i.translate(str.maketrans('', '', string.punctuation)) for i in message.text.lower().split(' ')} \
                        .intersection(set(ban_list)):
                    await message.delete()


        @dp.message()
        async def message_filter(message: types.Message):
            if message.chat.id == int(config("chat_id")):
                id_list1 = cursor.execute(f"SELECT id FROM id_list ")
                id_list = []
                for i in id_list1:
                    id_list.append(i[0])
                if message.from_user.id != int(config("admin_id")) and message.from_user.id not in id_list:
                    if message.content_type in ['audio', 'document', 'game', 'photo', 'video', 'video_note', 'voice', 'contact',
                                                'location', 'venue', 'invoice', 'successful_payment', 'connected_website',
                                                'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message',
                                                'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
                                                'passport_data', 'poll', 'dice', 'message_auto_delete_timer_changed',
                                                'video_chat_scheduled', 'video_chat_started', 'video_chat_ended',
                                                'video_chat_participants_invited', 'web_app_data', 'unknown', 'any']:
                        await message.delete()


        async def main():
            await dp.start_polling(bot)


        if __name__ == "__main__":
            asyncio.new_event_loop().run_until_complete(main())
    except:
        async def main():
            await dp.start_polling(bot)


        if __name__ == "main":
            asyncio.new_event_loop().run_until_complete(main())
