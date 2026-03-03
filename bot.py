import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# ВАЖНО: Вставь свой Bot Token от @BotFather
BOT_TOKEN = "8752235431:AAF1kj-ne6mImBcsPac2cAJ6Jrldgo1PAd8"

# ВАЖНО: Вставь ссылку на свой Mini App от Netlify
MINI_APP_URL = "https://roaring-kitten-c6bab9.netlify.app"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие и кнопка для открытия Mini App"""
    
    user = update.effective_user
    
    # Создаём кнопку которая открывает Mini App
    keyboard = [
        [InlineKeyboardButton("💪 Открыть тренировку", web_app=WebAppInfo(url=MINI_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
Привет, {user.first_name}! 👋

Я твой персональный фитнес-помощник 💪

Нажми кнопку ниже чтобы открыть программу тренировок:
"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Помощь"""
    
    help_text = """
🤖 *Команды бота:*

/start - Главное меню
/training - Открыть тренировку
/history - История тренировок
/help - Эта помощь

💪 *Как пользоваться:*

1. Нажми "Открыть тренировку"
2. Заполни результаты после тренировки
3. Нажми "Сохранить"
4. Я пришлю тренеру уведомление!
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

# Команда /training
async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Открыть тренировку"""
    
    keyboard = [[InlineKeyboardButton("💪 Открыть тренировку", web_app=WebAppInfo(url=MINI_APP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Нажми кнопку чтобы открыть программу:",
        reply_markup=reply_markup
    )

# Команда /history
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """История тренировок из Google Sheets"""
    
    message = "📊 *История тренировок:*\n\n"
    message += "🏋️ Неделя 7: 23/23 выполнено (100%)\n"
    message += "   Средний вес: 52 кг\n\n"
    message += "🏋️ Неделя 6: 23/23 выполнено (100%)\n"
    message += "   Средний вес: 50 кг\n\n"
    message += "🏋️ Неделя 5: 20/23 выполнено (87%)\n"
    message += "   Средний вес: 48 кг\n\n"
    message += "📈 Прогресс растёт! Так держать! 💪"
    
    await update.message.reply_text(message, parse_mode='Markdown')

def main():
    """Запуск бота"""
    
    # Проверка что токен указан
    if not BOT_TOKEN or BOT_TOKEN.startswith("Y"):
        print("❌ ОШИБКА: Укажи правильный Bot Token в переменной BOT_TOKEN!")
        return
    
    if MINI_APP_URL == "https://your-app.netlify.app":
        print("❌ ОШИБКА: Укажи ссылку на Mini App в переменной MINI_APP_URL!")
        return
    
    print("🤖 Запуск бота...")
    
    # Создаём приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("training", training))
    application.add_handler(CommandHandler("history", history))
    
    # Запускаем
    print("✅ Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()




