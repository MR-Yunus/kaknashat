from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests
import logging

# إعدادات البوت
TELEGRAM_TOKEN = '7511979228:AAGu0Qoi4Ejny_sLVbRsa4yyLzO6mtXCuOA'
SCREENSHOT_API_KEY = 'XQY7QG6-R5M4M5P-HMQGWAV-QKDZCJB'

# إعداد التسجيل للأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /start"""
    await update.message.reply_text(
        "Привет! Я бот для получения дорожных карт.\n"
        "Просто отправь мне название направления, например:\n"
        "• frontend\n• devops\n• ai\n\n"
        "Или используй команду /map <направление>"
    )

async def send_roadmap(update: Update, topic: str):
    """إرسال خريطة الطريق"""
    url = f"https://roadmap.sh/{topic}"
    screenshot_url = f"https://api.screenshotapi.net/screenshot?token={SCREENSHOT_API_KEY}&url={url}"
    
    try:
        # التحقق من أن الرابط يعمل قبل الإرسال
        response = requests.head(screenshot_url, timeout=10)
        if response.status_code == 200:
            await update.message.reply_photo(
                photo=screenshot_url,
                caption=f"🗺️ Дорожная карта: {topic.capitalize()}"
            )
        else:
            await update.message.reply_text(
                "⚠️ Не удалось загрузить карту. Попробуйте позже."
            )
    except Exception as e:
        logging.error(f"Error sending roadmap: {e}")
        await update.message.reply_text(
            "⚠️ Произошла ошибка. Пожалуйста, попробуйте другой раздел."
        )

async def roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /map"""
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажите направление, например: /map ai")
        return
    
    topic = context.args[0].lower()
    await send_roadmap(update, topic)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل النصية العادية"""
    topic = update.message.text.lower()
    await send_roadmap(update, topic)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # تسجيل المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("map", roadmap))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # تشغيل البوت
    app.run_polling()
