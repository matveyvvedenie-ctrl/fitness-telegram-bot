import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# ВАЖНО: Вставь свой Bot Token от @BotFather
BOT_TOKEN = "8752235431:AAF1kj-ne6mImBcsPac2cAJ6Jrldgo1PAd8"

# ВАЖНО: Вставь ссылку на свой Mini App от Netlify
MINI_APP_URL = "https://tubular-dango-355051.netlify.app"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие и кнопка для открытия Mini App"""
    
    user = update.effective_user
    
    # Создаём кнопку которая открывает Mini App
    keyboard = [
        [InlineKeyboardButton("💪 Открыть тренировку", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton("📊 Мой прогресс", callback_data="progress")],
        [InlineKeyboardButton("📚 История", callback_data="history")]
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
/progress - Мой прогресс  
/history - История тренировок
/help - Эта помощь

💪 *Как пользоваться:*

1. Нажми "Открыть тренировку"
2. Заполни результаты после тренировки
3. Нажми "Сохранить"
4. Я пришлю тренеру уведомление!

❓ Вопросы? Напиши @твой_telegram
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

# Команда /progress
async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Прогресс (заглушка, потом подключим реальные данные)"""
    
    await update.message.reply_text(
        """
📊 *Твой прогресс:*

На этой неделе:
✅ Выполнено: 18 из 36 подходов
📈 Прогресс: 50%
🔥 Streak: 4 недели подряд

💪 Так держать!
""",
        parse_mode='Markdown'
    )

# Команда /history
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """История (заглушка)"""
    
    await update.message.reply_text(
        """
📚 *История тренировок:*

Неделя 7 (текущая): 50%
Неделя 6: 100% ✅
Неделя 5: 95%
Неделя 4: 100% ✅

🏆 Всего недель: 7
💪 Всего подходов: 234
""",
        parse_mode='Markdown'
    )

def main():
    """Запуск бота"""
    
    # Проверка что токен указан
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ОШИБКА: Укажи Bot Token в переменной BOT_TOKEN!")
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
    application.add_handler(CommandHandler("progress", progress))
    application.add_handler(CommandHandler("history", history))
    
    # Запускаем
    print("✅ Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()



