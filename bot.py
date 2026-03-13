import os
import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import datetime

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# URL Mini App
MINI_APP_URL = "https://tubular-dango-355051.netlify.app"

# Мотивационные сообщения
MOTIVATIONAL_MESSAGES = [
    "💪 Помни: каждая тренировка приближает тебя к цели!",
    "🔥 Ты сильнее, чем думаешь! Продолжай в том же духе!",
    "⚡ Прогресс — это сумма маленьких усилий, повторяемых день за днём!",
    "🏆 Чемпионы делают то, что другие не хотят делать!",
    "💯 Каждая капля пота — инвестиция в твоё будущее!",
    "🎯 Твоё тело слышит всё, что говорит твой разум. Оставайся позитивным!",
    "🌟 Единственная плохая тренировка — та, которую ты пропустил!",
    "💎 Боль временна, гордость вечна!"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    welcome_text = f"""
👋 Привет, {user.first_name}!

Я твой фитнес-помощник! 💪

🏋️ Открой тренировку: /training
📊 Посмотри прогресс: /progress
📜 История: /history
⏰ Напоминания: /reminder

Начни с /training! 🚀
    """
    
    await update.message.reply_text(welcome_text)
    logger.info(f"User {user.id} ({user.first_name}) started the bot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    help_text = """
🤖 <b>Доступные команды:</b>

/start - Начать работу с ботом
/training - Открыть тренировку
/history - История тренировок
/progress - Статистика и прогресс
/reminder ЧЧ:ММ - Установить напоминание
/help - Показать это сообщение

💡 <b>Примеры использования:</b>

/reminder 09:00 - напоминание в 9 утра
/reminder 18:30 - напоминание в 18:30
/reminder off - отключить напоминания

📱 Нажми /training чтобы начать тренировку!
    """
    
    await update.message.reply_text(help_text, parse_mode='HTML')

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /training - открывает Mini App"""
    keyboard = [
        [InlineKeyboardButton(
            "💪 Открыть тренировку",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🏋️ <b>Твоя тренировка готова!</b>\n\n"
        "Нажми кнопку ниже чтобы открыть программу:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /history"""
    await update.message.reply_text(
        "📜 <b>История тренировок</b>\n\n"
        "Ты делаешь отличную работу! 💪\n"
        "Каждая тренировка приближает тебя к цели!\n\n"
        "Посмотри детальную статистику: /progress",
        parse_mode='HTML'
    )

async def progress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /progress"""
    keyboard = [
        [InlineKeyboardButton(
            "📊 Открыть статистику",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📊 <b>Твой прогресс</b>\n\n"
        "Открой Mini App чтобы посмотреть:\n"
        "• Графики прогресса\n"
        "• Личные рекорды\n"
        "• Статистику по неделям\n\n"
        "Нажми кнопку ниже:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

# ===== УВЕДОМЛЕНИЯ =====

async def send_workout_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Напоминание о тренировке"""
    chat_id = context.job.chat_id
    
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text="⏰ <b>Время тренировки!</b>\n\n"
                 "Не забудь выполнить сегодняшнюю программу! 💪\n\n"
                 "Открой /training чтобы начать!",
            parse_mode='HTML'
        )
    except Exception as e:
        logger.error(f"Ошибка отправки напоминания: {e}")

async def send_motivational_message(context: ContextTypes.DEFAULT_TYPE):
    """Случайное мотивационное сообщение"""
    chat_id = context.job.chat_id
    
    import random
    message = random.choice(MOTIVATIONAL_MESSAGES)
    
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=message
        )
    except Exception as e:
        logger.error(f"Ошибка отправки мотивации: {e}")

def schedule_workout_reminder(chat_id: int, hour: int, minute: int, application):
    """Установить ежедневное напоминание"""
    job_queue = application.job_queue
    
    # Удаляем старые напоминания для этого пользователя
    current_jobs = job_queue.get_jobs_by_name(f'workout_reminder_{chat_id}')
    for job in current_jobs:
        job.schedule_removal()
    
    # Создаём время напоминания
    reminder_time = datetime.time(hour=hour, minute=minute, tzinfo=datetime.timezone.utc)
    
    # Добавляем новое ежедневное напоминание
    job_queue.run_daily(
        send_workout_reminder,
        time=reminder_time,
        chat_id=chat_id,
        name=f'workout_reminder_{chat_id}'
    )
    
    logger.info(f"Установлено напоминание для {chat_id} на {hour}:{minute:02d}")

async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Установить время напоминания о тренировке"""
    chat_id = update.effective_chat.id
    
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "⏰ <b>Напоминания о тренировке</b>\n\n"
            "Используй: /reminder ЧЧ:ММ\n\n"
            "Примеры:\n"
            "/reminder 09:00 — напоминание в 9 утра\n"
            "/reminder 18:30 — напоминание в 18:30\n"
            "/reminder off — отключить напоминания",
            parse_mode='HTML'
        )
        return
    
    time_arg = context.args[0]
    
    if time_arg.lower() == 'off':
        # Отключаем напоминания
        jobs = context.application.job_queue.get_jobs_by_name(f'workout_reminder_{chat_id}')
        for job in jobs:
            job.schedule_removal()
        
        await update.message.reply_text("✅ Напоминания отключены!")
        return
    
    try:
        hour, minute = map(int, time_arg.split(':'))
        
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Неверное время")
        
        schedule_workout_reminder(chat_id, hour, minute, context.application)
        
        await update.message.reply_text(
            f"✅ Напоминание установлено!\n\n"
            f"⏰ Буду напоминать о тренировке каждый день в {hour:02d}:{minute:02d}",
            parse_mode='HTML'
        )
        
    except ValueError:
        await update.message.reply_text(
            "❌ Неверный формат времени!\n\n"
            "Используй формат ЧЧ:ММ\n"
            "Например: /reminder 09:00"
        )

def main():
    """Запуск бота"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN не установлен!")
        return
    
    application = Application.builder().token(token).build()
    
    # Регистрация команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("training", training))
    application.add_handler(CommandHandler("history", history))
    application.add_handler(CommandHandler("progress", progress_command))
    application.add_handler(CommandHandler("reminder", set_reminder))
    
    logger.info("Бот запущен!")
    
    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()













