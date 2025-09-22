# asyncio - встроенная библиотека Python для асинхронного программирования
import asyncio
import os
# aiogram.Dispatcher - диспетчер событий из библиотеки aiogram для Telegram ботов
from aiogram import Dispatcher
# aiogram.filters - модуль фильтров для обработки команд и сообщений
# Command - фильтр для команд типа /start, /login
# Без этого: не работает парсинг аргументов
from aiogram.filters import Command, CommandObject
# asgiref.sync.sync_to_async - адаптер для вызова синхронного кода из асинхронного
# Позволяет использовать Django ORM (синхронный) в асинхронных функциях бота
# Без этого: невозможна работа с базой данных Django из асинхронного кода
from asgiref.sync import sync_to_async
# Конфигурация Django для запуска ORM вне веб-приложения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ste.settings')
import django  # Основной модуль Django фреймворка
django.setup()  # Инициализация Django приложения
# TelegramProfile - модель связи пользователей с Telegram
from stem.models import Task, TelegramProfile
# django.contrib.auth.models.User - встроенная модель пользователей Django
from django.contrib.auth.models import User
from ste.settings import BOT
# django.utils.timezone - модуль работы с временными зонами Django
from django.utils import timezone

# Функция для проверки авторизации пользователя по chat_id
@sync_to_async  # декоратор - преобразует синхронную функцию в асинхронную
def get_user_by_chat_id(chat_id):
    """Получает пользователя Django по Telegram chat_id"""
    try:
        return TelegramProfile.objects.get(telegram_chat_id=chat_id).user  # objects.get() - метод получения одного объекта из БД
    except TelegramProfile.DoesNotExist:  # DoesNotExist - исключение когда объект не найден в БД
        return None

# Функция для авторизации пользователя по уникальному 10-значному ID
@sync_to_async
def authorize_user(unique_id, chat_id):  # unique_id - переменная с 10-значным ID для авторизации
    """Связывает Telegram chat_id с профилем пользователя через unique_id"""
    try:
        profile = TelegramProfile.objects.get(unique_id=unique_id)  # получаем профиль по уникальному ID
        profile.telegram_chat_id = chat_id  # chat_id - переменная с ID чата в Telegram
        profile.save()  # save() - метод сохранения изменений в БД
        return profile.user
    except TelegramProfile.DoesNotExist:  # исключение - профиль с таким ID не найден
        return None

# Функция для отвязки Telegram бота от профиля пользователя
@sync_to_async
def disconnect_user(chat_id):
    """Отвязывает Telegram chat_id от профиля пользователя (устанавливает None)"""
    try:
        profile = TelegramProfile.objects.get(telegram_chat_id=chat_id)
        user = profile.user
        profile.telegram_chat_id = None  # Отвязываем chat_id
        profile.save()
        return user
    except TelegramProfile.DoesNotExist:
        return None

# Универсальная функция для получения задач с различными фильтрами
@sync_to_async
def get_user_tasks_filtered(user, task_type="all"):  # task_type="all" - параметр по умолчанию для типа задач
    """Универсальная функция для получения задач с фильтрацией по типу"""
    if not user:
        return "❌ Авторизуйтесь командой `/login ВАШ_ID`"
    
    # Определяем фильтр и заголовок в зависимости от типа
    filters = {'user': user, 'completed': False}  # filters - словарь с параметрами фильтрации
    
    if task_type == "notes":  # task_type - переменная определяющая тип задач
        filters['reminder_time__isnull'] = True  # reminder_time__isnull - фильтр Django для NULL значений
        title = "📝 *Ваши заметки:*"
        empty_msg = "📝 *Заметки:*\n\nУ вас нет активных заметок."
    elif task_type == "reminders":
        filters['reminder_time__isnull'] = False  # False - задачи с установленным временем напоминания
        title = "⏰ *Ваши напоминания:*"
        empty_msg = "⏰ *Напоминания:*\n\nУ вас нет активных напоминаний."
    
    tasks = Task.objects.filter(**filters)  # Task.objects.filter(**filters) - метод фильтрации задач по параметрам
    if not tasks:
        return empty_msg
    
    result = f"{title}\n\n"
    for task in tasks:
        if task_type == "notes":
            result += f"📝 *{task.title}*\n"
            if task.description:  # description - поле модели с описанием задачи
                result += f"_{task.description}_\n"
            result += f"📅 Создано: {task.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        elif task_type == "reminders":
            icon = "❗️" if task.overdue else "⏰"  # overdue - boolean поле статуса просрочки
            status = "Просрочено" if task.overdue else "Активно"  # переменная статуса для отображения
            result += f"{icon} *{task.title}*\n"
            if task.description:  # проверка наличия описания задачи
                result += f"_{task.description}_\n"
            result += f"📅 Создано: {task.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            result += f"⏰ Напоминание: {task.reminder_time.strftime('%d.%m.%Y %H:%M')}\n"
            result += f"Статус: {status}\n\n"
    
    return result

# Функция для получения всех задач пользователя с разделением по категориям
@sync_to_async
def get_all_tasks(user):
    """Возвращает все задачи пользователя, разделенные на активные, просроченные и завершенные"""
    if not user:
        return "❌ Авторизуйтесь командой `/login ВАШ_ID`"
    
    all_tasks = Task.objects.filter(user=user)
    if not all_tasks:
        return "📋 *Все задачи:*\n\nУ вас пока нет задач."
    
    # Разделяем задачи по категориям для удобного отображения
    active = all_tasks.filter(completed=False, overdue=False)
    overdue = all_tasks.filter(overdue=True, completed=False)
    completed = all_tasks.filter(completed=True)
    
    result = "📋 *Все ваши задачи:*\n\n"
    
    # Отображаем активные задачи
    if active:
        result += "🟢 *АКТИВНЫЕ:*\n"
        result += "\n".join(f"{'⏰' if t.reminder_time else '📝'} {t.title}" for t in active) + "\n\n"
    
    # Отображаем просроченные задачи
    if overdue:
        result += "🔴 *ПРОСРОЧЕННЫЕ:*\n"
        result += "\n".join(f"❗️ {t.title}" for t in overdue) + "\n\n"
    
    # Отображаем завершенные задачи
    if completed:
        result += "✅ *ЗАВЕРШЕННЫЕ:*\n"
        result += "\n".join(f"✅ {t.title}" for t in completed) + "\n\n"
    
    # Добавляем статистику
    result += f"📊 *Статистика:* Всего: {all_tasks.count()} | Активных: {active.count()} | Просроченных: {overdue.count()} | Завершенных: {completed.count()}"
    return result

# Функция для проверки и отправки напоминаний
@sync_to_async
def get_pending_notifications():
    """Получает список напоминаний, которые нужно отправить"""
    # Django уже настроен на московское время в settings.py
    now = timezone.now()
    
    # Ищем напоминания, время которых уже наступило
    pending_tasks = Task.objects.filter(
        reminder_time__lte=now,  # Время напоминания <= текущее время
        reminder_time__isnull=False,   # У задачи есть время напоминания
        notification_sent=False,       # Уведомление еще не отправлено
        completed=False                # Задача не завершена
    ).select_related('user__telegramprofile')  # Оптимизируем запрос
    
    return list(pending_tasks)

# Функция для отметки уведомления как отправленного
@sync_to_async
def mark_notification_sent(task_id):
    """Помечает уведомление как отправленное"""
    try:
        task = Task.objects.get(id=task_id)
        task.notification_sent = True
        task.save()
        return True
    except Task.DoesNotExist:
        return False

# Функция для отправки уведомления пользователю
async def send_notification(task):  # async функция - асинхронная функция для отправки уведомлений
    """Отправляет уведомление о напоминании пользователю в Telegram"""
    try:  # try блок - обработка исключений
        # Проверяем подключение Telegram
        if not (hasattr(task.user, 'telegramprofile') and task.user.telegramprofile.telegram_chat_id):  # hasattr() - функция проверки наличия атрибута у объекта
            return False
        
        chat_id = task.user.telegramprofile.telegram_chat_id  # переменная с ID чата для отправки сообщения
        
        # Формируем компактное сообщение с напоминанием
        desc_text = f"\n📝 _{task.description}_\n" if task.description else ""  # условное выражение для описания
        message = (  # переменная с текстом сообщения
            f"⏰ *НАПОМИНАНИЕ!*\n\n🔔 *{task.title}*\n{desc_text}"
            f"\n📅 Создано: {timezone.localtime(task.created_at).strftime('%d.%m.%Y %H:%M')}\n"  # localtime() - функция преобразования времени в локальный часовой пояс
            f"⏰ Время: {timezone.localtime(task.reminder_time).strftime('%d.%m.%Y %H:%M')}\n\n"
            f"💡 Команда `/tasksTime` покажет все напоминания"
        )
        
        # Отправляем уведомление и помечаем как отправленное
        await BOT.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')  # BOT.send_message() - метод отправки сообщений в Telegram; parse_mode='Markdown' - параметр форматирования текста
        await mark_notification_sent(task.id)  # mark_notification_sent() - функция отметки уведомления как отправленного
        return True
        
    except Exception as e:  # Exception - базовый класс всех исключений Python
        print(f"Ошибка отправки уведомления для задачи {task.id}: {e}")  # вывод ошибки в консоль
        return False

# Основная функция проверки и отправки напоминаний
async def check_and_send_notifications():  # функция проверки и отправки уведомлений
    """Проверяет и отправляет все pending уведомления"""
    try:
        pending_tasks = await get_pending_notifications()  # получаем список задач для уведомлений
        if not pending_tasks:
            return
        
        print(f"📤 Найдено {len(pending_tasks)} напоминаний для отправки")
        
        # Отправляем уведомления с паузой между отправками
        for task in pending_tasks:  # цикл по каждой задаче
            status = "✅" if await send_notification(task) else "❌"  # переменная статуса отправки
            print(f"{status} {task.title} -> {task.user.username}")
            await asyncio.sleep(0.5)  # sleep() - функция паузы на 0.5 секунды
            
    except Exception as e:  # обработка любых ошибок в функции
        print(f"❌ Ошибка в check_and_send_notifications: {e}")

# Фоновая задача для периодической проверки напоминаний
async def notification_worker():  # фоновая задача для проверки напоминаний
    """Фоновая задача проверки напоминаний каждые 60 секунд"""
    print("🔔 Запущен сервис напоминаний (проверка каждые 60 секунд)")
    while True:  # бесконечный цикл работы
        try:
            await check_and_send_notifications()
        except Exception as e:  # перехват любых ошибок в цикле
            print(f"❌ Ошибка в notification_worker: {e}")
        finally:  # finally блок - выполняется в любом случае
            await asyncio.sleep(60)  # пауза 60 секунд между проверками

# Создаём диспетчер для обработки сообщений
dp = Dispatcher() 

# Обработчик команды /start - проверяет соединение и приветствует пользователя
@dp.message(Command("start"))  # @dp.message() - декоратор обработчика сообщений; Command("start") - фильтр для команды /start
async def command_start_handler(message):  # обработчик команды - async функция
    """Главная команда - проверяет авторизацию и показывает статус соединения"""
    user = await get_user_by_chat_id(message.chat.id)  # message.chat.id - переменная с ID чата пользователя
    
    if not user:
        # Пользователь не авторизован - показываем инструкцию
        await message.answer(  # answer() - метод отправки ответа пользователю
            "🤖 *Добро пожаловать в STEM Bot!*\n\n"
            "❌ *Соединение не установлено*\n\n"
            "Для получения доступа к вашим заметкам и напоминаниям необходимо авторизоваться.\n\n"
            "📋 *Инструкция:*\n"
            "1. Зарегистрируйтесь на сайте\n"
            "2. Откройте ваш профиль\n"  
            "3. Скопируйте ваш 10-значный ID\n"
            "4. Введите: `/login ВАШ_ID`\n\n"
            "Пример: `/login 1234567890`",
            parse_mode='Markdown'  # параметр форматирования сообщения
        )
    else:
        # Пользователь авторизован - показываем приветствие и команды
        await message.answer(
            f"🤖 *Добро пожаловать, {user.username}!*\n\n"
            f"✅ *Соединение установлено*\n\n"
            f"📋 *Доступные команды:*\n"
            f"/tasks - заметки (без времени)\n"
            f"/tasksTime - напоминания (с временем)\n"
            f"/taskAll - все задачи\n" 
            f"/logout - отключить бота\n"
            f"/help - помощь",
            parse_mode='Markdown'
        )

# Обработчик команды /login - авторизует пользователя по уникальному ID
@dp.message(Command("login"))  # декоратор обработчика команды /login
async def command_login_handler(message, command: CommandObject):  # CommandObject - класс объекта команды с параметрами
    """Команда для связывания Telegram аккаунта с профилем на сайте через 10-значный ID"""
    if not command.args:  # args - переменная с аргументами команды
        await message.answer(  # отправка ответного сообщения
            "❌ *Ошибка!* Укажите ваш 10-значный ID.\n\n"
            "Пример: `/login 1234567890`\n\n"
            "ID можно найти в вашем профиле на сайте.",
            parse_mode='Markdown'
        )
        return
    
    try:
        unique_id = int(command.args.strip())
        # Проверяем, что ID состоит именно из 10 цифр
        if len(str(unique_id)) != 10:
            await message.answer(
                "❌ *Ошибка!* ID должен состоять из 10 цифр.\n\n"
                "Пример: `/login 1234567890`",
                parse_mode='Markdown'
            )
            return
            
        # Пытаемся авторизовать пользователя
        user = await authorize_user(unique_id, message.chat.id)
        
        if user:
            # Успешная авторизация
            await message.answer(
                f"✅ *Успешная авторизация!*\n\n"
                f"Добро пожаловать, {user.username}!\n"
                f"Ваш аккаунт подключен к Telegram боту.\n\n"
                f"📋 *Доступные команды:*\n"
                f"/start - главная страница\n"
                f"/tasks - заметки (без времени)\n"
                f"/tasksTime - напоминания (с временем)\n"
                f"/taskAll - все задачи\n"
                f"/logout - отключить бота\n"
                f"/help - помощь",
                parse_mode='Markdown'
            )
        else:
            # Неверный ID
            await message.answer(
                "❌ *Неверный ID!*\n\n"
                "Проверьте правильность 10-значного ID в вашем профиле на сайте.",
                parse_mode='Markdown'
            )
    except ValueError:
        # ID содержит не только цифры
        await message.answer(
            "❌ *Ошибка!* ID должен содержать только цифры.\n\n"
            "Пример: `/login 1234567890`",
            parse_mode='Markdown'
        )

# Обработчик команды /tasks - показывает заметки (без времени)
@dp.message(Command("tasks"))
async def command_tasks_handler(message):
    """Команда для просмотра заметок (задачи без времени напоминания)"""
    user = await get_user_by_chat_id(message.chat.id)
    notes = await get_user_tasks_filtered(user, "notes")
    await message.answer(notes, parse_mode='Markdown')

# Обработчик команды /tasksTime - показывает напоминания (с временем)
@dp.message(Command("tasksTime"))
async def command_tasks_time_handler(message):
    """Команда для просмотра напоминаний (задачи с временем напоминания)"""
    user = await get_user_by_chat_id(message.chat.id)
    reminders = await get_user_tasks_filtered(user, "reminders")
    await message.answer(reminders, parse_mode='Markdown')

# Обработчик команды /taskAll - показывает все задачи с разделением по категориям
@dp.message(Command("taskAll"))
async def command_task_all_handler(message):
    """Команда для просмотра всех задач пользователя, разделенных по статусу"""
    user = await get_user_by_chat_id(message.chat.id)
    tasks = await get_all_tasks(user)
    await message.answer(tasks, parse_mode='Markdown')

# Обработчик команды /help - показывает справку по командам
@dp.message(Command("help"))
async def command_help_handler(message):
    """Команда справки - показывает все доступные команды и инструкцию по использованию"""
    await message.answer(
        "🤖 *STEM Bot - Помощь*\n\n"
        "📋 *Команды:*\n"
        "/start - проверка соединения\n"
        "/login ID - авторизация (10 цифр)\n"
        "/tasks - заметки (без времени)\n"
        "/tasksTime - напоминания (с временем)\n"
        "/taskAll - все задачи (с разделением)\n"
        "/logout - отключить бота\n"
        "/help - эта помощь\n\n"
        "📝 *Типы задач:*\n"
        "• *Заметки* - обычные задачи без времени\n"
        "• *Напоминания* - задачи с установленным временем\n\n"
        "💡 *Как начать:*\n"
        "1. Зарегистрируйтесь на сайте\n"
        "2. В профиле найдите 10-значный ID\n"
        "3. Используйте `/login ВАШ_ID`\n"
        "4. Наслаждайтесь уведомлениями!\n\n"
        "🔌 *Управление подключением:*\n"
        "• `/logout` - отвязать бота от профиля\n"
        "• После отключения можно снова подключиться через `/login`",
        parse_mode='Markdown'
    )

# Обработчик команды /logout - отвязывает бота от профиля пользователя
@dp.message(Command("logout"))
async def command_logout_handler(message):
    """Команда для отвязки Telegram бота от профиля пользователя"""
    user = await get_user_by_chat_id(message.chat.id)
    
    if not user:
        # Пользователь уже не авторизован
        await message.answer(
            "❌ *Вы не авторизованы*\n\n"
            "Бот уже отключен от вашего профиля.\n"
            "Для подключения используйте `/login ВАШ_ID`",
            parse_mode='Markdown'
        )
        return
    
    # Отвязываем пользователя
    disconnected_user = await disconnect_user(message.chat.id)
    
    if disconnected_user:
        # Успешно отвязан
        await message.answer(
            f"✅ *Бот успешно отключен!*\n\n"
            f"Пользователь {disconnected_user.username}, ваш Telegram бот отвязан от профиля на сайте.\n\n"
            f"🔄 *Для повторного подключения:*\n"
            f"1. Найдите ваш 10-значный ID в профиле на сайте\n"
            f"2. Используйте команду `/login ВАШ_ID`\n\n"
            f"💡 Ваш профиль и задачи остались на сайте без изменений.",
            parse_mode='Markdown'
        )
    else:
        # Ошибка отвязки (не должно происходить, но на всякий случай)
        await message.answer(
            "❌ *Ошибка отключения*\n\n"
            "Произошла ошибка при отключении бота. Попробуйте еще раз.",
            parse_mode='Markdown'
        )

# Основная функция запуска бота с сервисом напоминаний
async def main():
    """Главная функция для запуска бота и сервиса напоминаний"""
    # Запускаем фоновую задачу проверки напоминаний
    asyncio.create_task(notification_worker())
    
    # Запускаем основной polling бота
    print("🤖 Запуск Telegram бота...")
    await dp.start_polling(BOT)

# Запуск бота - точка входа в приложение
if __name__ == "__main__":  # условие запуска при прямом выполнении файла
    try:
        asyncio.run(main())  # запуск основной асинхронной функции
    except KeyboardInterrupt:  # KeyboardInterrupt - исключение при нажатии Ctrl+C
        print("\n🛑 Бот остановлен")
    except Exception as e:  # обработка любых других критических ошибок
        print(f"❌ Критическая ошибка: {e}")