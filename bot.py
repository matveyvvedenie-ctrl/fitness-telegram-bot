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
    
    try:
        creds_json = os.environ.get('GOOGLE_CREDENTIALS')
        
        if not creds_json:
            await update.message.reply_text("❌ Переменная НЕ найдена")
            return
        
        length = len(creds_json)
        await update.message.reply_text(f"✅ Переменная найдена! Длина: {length} символов")

        # Подключаемся к Google Sheets
        creds_dict = json.loads(creds_json)
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # Открываем таблицу
        sheet = client.open('Smart_Training_Tracker').worksheet('Архив')
        
        # Читаем данные
        records = sheet.get_all_records()
        
        if not records:
            await update.message.reply_text("📊 История пуста. Завершите первую тренировку!")
            return
        
        # Формируем сообщение
        message = "📊 *История тренировок:*\n\n"
        
        for record in records[-5:]:  # Последние 5 записей
            message += f"🏋️ {record['Неделя']}: {record['Выполнено']}/{record['Всего']} ({record['Процент']})\n"
            message += f"   Средний вес: {record['Средний вес']}\n\n"
        
        message += "📈 Отличная работа! Продолжай в том же духе! 💪"
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    except Exception as e:
        print(f"Ошибка чтения истории: {e}")
        await update.message.reply_text("❌ Не удалось загрузить историю")

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





