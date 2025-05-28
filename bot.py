from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests
import logging

# إعدادات البوت
TELEGRAM_TOKEN = '7511979228:AAGu0Qoi4Ejny_sLVbRsa4yyLzO6mtXCuOA'
SCREENSHOT_API_KEY = 'XQY7QG6-R5M4M5P-HMQGWAV-QKDZCJB'

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /start"""
    start_text = (
        "Привет! Я бот для получения дорожных карт.\n\n"
        "Как использовать:\n"
        "1. Просто напиши название направления (например: ai)\n"
        "2. Или используй команду /map <направление>\n\n"
        "Доступные направления: frontend, backend, devops, ai, android, etc."
    )
    await update.message.reply_text(start_text)

async def get_roadmap_image(topic: str):
    """جلب صورة الخريطة من API"""
    url = f"https://roadmap.sh/{topic}"
    api_url = f"https://api.screenshotapi.net/screenshot?token={SCREENSHOT_API_KEY}&url={url}&full_page=true&delay=2000"
    
    try:
        response = requests.get(api_url, timeout=20)
        response.raise_for_status()
        return api_url  # نرجع الرابط مباشرة حيث أن API يعيد رابط الصورة
    except Exception as e:
        logger.error(f"API Error for {topic}: {e}")
        return None

async def send_roadmap_response(update: Update, topic: str):
    """إرسال الرد المناسب"""
    valid_topics = ['frontend', 'backend', 'devops', 'ai', 'android', 'react', 'java', 'python']
    
    if topic not in valid_topics:
        await update.message.reply_text("⚠️ Неизвестное направление. Попробуйте одно из этих:\n" + "\n".join(valid_topics))
        return

    await update.message.reply_text("🔄 Загружаю карту...")
    
    image_url = await get_roadmap_image(topic)
    
    if image_url:
        try:
            await update.message.reply_photo(
                photo=image_url,
                caption=f"🗺 Дорожная карта: {topic.capitalize()}"
            )
        except Exception as e:
            logger.error(f"Telegram send error: {e}")
            await update.message.reply_text("⚠️ Ошибка при отправке изображения")
    else:
        await update.message.reply_text("⚠️ Не удалось получить карту. Попробуйте позже или другой раздел.")

async def roadmap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /map"""
    if not context.args:
        await update.message.reply_text("ℹ️ Пожалуйста, укажите направление после команды /map\nНапример: /map ai")
        return
    
    topic = context.args[0].lower()
    await send_roadmap_response(update, topic)

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل النصية"""
    topic = update.message.text.lower().strip()
    await send_roadmap_response(update, topic)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # تسجيل المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("map", roadmap_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
    
    # إعدادات إضافية
    app.add_error_handler(lambda update, context: logger.error(f"Update {update} caused error {context.error}"))
    
    logger.info("Starting bot...")
    app.run_polling()
