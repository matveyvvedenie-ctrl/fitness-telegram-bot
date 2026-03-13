import os
import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# URL Mini App
MINI_APP_URL = "https://tubular-dango-355051.netlify.app"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    
    welcome_text = f"""
👋 Привет, {user.first_name}!

Я твой фитнес-помощник! 💪

🏋️ Открой тренировку: /training
📊 Посмотри прогресс: /progress
📜 История: /history

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
/help - Показать это сообщение

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
    
    logger.info("Бот запущен!")
    
    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
