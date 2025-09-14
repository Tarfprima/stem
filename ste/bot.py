# Импортируем библиотеки для Telegram-бота 
import asyncio
from aiogram import Dispatcher
from aiogram.filters import Command

# Подключаем Django, для доступа к настройкам и базе данных
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ste.settings')
import django
django.setup()

# Импортируем модель Task из приложения stem (для получения заметок и напоминаний)
from stem.models import Task

# Импортируем объект BOT из settings.py (созданный там с токеном)
from ste.settings import BOT

# Импортируем sync_to_async для асинхронного доступа к синхронной БД Django
from asgiref.sync import sync_to_async

# Функция для получения данных из базы 
@sync_to_async
def get_data():
    result = ''  # Пустая строка для хранения ответа
    for t in Task.objects.all():  # Проходим по всем задачам в базе
        result += f"\n --- ЗАДАЧА ---\n *{t.title}* \n Описание: _{t.description if t.description else 'Нет описания'}_ \n Время создания: {t.created_at} \n Напоминание: {t.reminder_time if t.reminder_time else 'Нет'} \n Статус: {'Завершено' if t.completed else 'Активно'}\n"  # Формируем текст с данными задачи
    return result

# Создаём диспетчер для обработки сообщений
dp = Dispatcher()

# Обработчик команды /start 
@dp.message(Command("start"))
async def command_start_handler(message):
    print('Ура! Мне написал', message.chat.id)  # Выводим в консоль ID пользователя
    print('Его фраза', message.text)  # Выводим текст сообщения
    tasks = await get_data()  # Получаем данные из базы асинхронно
    await message.answer(  # Отправляем ответ пользователю
        "Ваши заметки и напоминания:\n" + tasks, parse_mode='Markdown')  # Используем Markdown для форматирования

asyncio.run(  # Запуск асинхронной функции
    dp.start_polling(  # Диспетчер начинает обмен сообщениями
        BOT))  # Используя объект бота