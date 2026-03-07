import os
import json
from urllib.request import urlopen
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# ВАЖНО: Вставь свой Bot Token от @BotFather
BOT_TOKEN = "8752235431:AAF1kj-ne6mImBcsPac2cAJ6Jrldgo1PAd8"

# ВАЖНО: Вставь ссылку на свой Mini App от Netlify
MINI_APP_URL = "https://tubular-dango-355051.netlify.app"

# ВАЖНО: Вставь URL твоего Apps Script
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyqpppW2wnxH4nAYrZDaIu0XedFB5wfOeUXXokxFz4TpslB-GqD24B9GsPp0i_nTJ4GVA/exec"

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
/progress - Твой прогресс
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
    """История тренировок - мотивация"""
    
    message = """
📊 *История тренировок*

🏆 Ты делаешь отличную работу!

💪 Твой прогресс сохраняется автоматически.
Тренер видит все твои результаты и следит за динамикой.

📈 Продолжай тренироваться — результаты не заставят себя ждать!

🔥 Каждая тренировка приближает тебя к цели!
"""
    
    await update.message.reply_text(message, parse_mode='Markdown')

# Команда /progress
async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Статистика прогресса из Google Sheets"""
    
    try:
        # Получаем Chat ID пользователя
        chat_id = update.effective_user.id
        
        # Запрос к Apps Script
        url = f"{APPS_SCRIPT_URL}?action=progress&chatId={chat_id}"
        
        response = urlopen(url)
        data = json.loads(response.read())
        
        if data.get('status') == 'success':
            stats = data.get('data', {})
            
            weeks_total = stats.get('weeksTotal', 0)
            weeks_completed = stats.get('weeksCompleted', 0)
            completion_rate = stats.get('completionRate', 0)
            total_exercises = stats.get('totalExercises', 0)
            avg_weight = stats.get('avgWeight', 0)
            
            message = f"""
📊 *Твой прогресс*

🏆 Тренируешься: {weeks_total} недель
✅ Завершено: {weeks_completed} тренировочных недель ({completion_rate}%)
💪 Выполнено упражнений: {total_exercises}
📈 Средний вес: {avg_weight} кг

Продолжай в том же духе! 🔥
"""
        else:
            message = "❌ Не удалось загрузить статистику"
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    except Exception as e:
        print(f"Ошибка чтения прогресса: {e}")
        await update.message.reply_text("❌ Не удалось загрузить статистику")

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
    application.add_handler(CommandHandler("progress", progress))
    
    # Запускаем
    print("✅ Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()












