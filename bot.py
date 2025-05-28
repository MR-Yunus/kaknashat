from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests
import logging
from urllib.parse import quote

# إعدادات البوت
TELEGRAM_TOKEN = '7511979228:AAGu0Qoi4Ejny_sLVbRsa4yyLzO6mtXCuOA'
SCREENSHOT_API_KEY = 'XQY7QG6-R5M4M5P-HMQGWAV-QKDZCJB'
ROADMAP_BASE_URL = "https://roadmap.sh/"

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = (
        "🚀 Привет! Я бот для IT-дорожных карт\n\n"
        "Отправь мне название направления:\n"
        "• frontend\n• backend\n• devops\n• ai\n• android\n"
        "Или используй /map <направление>"
    )
    await update.message.reply_text(start_text)

async def get_roadmap_image(topic: str):
    """الحصول على صورة الخريطة مع الروابط الصحيحة"""
    try:
        # الرابط الصحيح حسب الموقع الرسمي
        roadmap_url = f"{ROADMAP_BASE_URL}{topic}"
        
        # استخدام واجهة التصوير
        encoded_url = quote(roadmap_url)
        api_url = f"https://api.screenshotapi.net/screenshot?token={SCREENSHOT_API_KEY}&url={encoded_url}&full_page=true&delay=3000"
        
        # التحقق من وجود الصفحة أولاً
        check_response = requests.head(roadmap_url, timeout=5)
        if check_response.status_code != 200:
            return None
            
        response = requests.get(api_url, timeout=15)
        if response.status_code == 200:
            return api_url
            
        return None
    except Exception as e:
        logger.error(f"Error getting roadmap: {e}")
        return None

async def handle_roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE, topic: str):
    """معالجة طلب الخريطة"""
    valid_topics = {
        'frontend', 'backend', 'devops', 'ai', 'android',
        'react', 'java', 'python', 'javascript', 'golang'
    }
    
    if topic not in valid_topics:
        await update.message.reply_text(
            "❌ Неизвестное направление. Доступные:\n" +
            "\n".join(f"• {t}" for t in sorted(valid_topics))
        )
        return

    loading_msg = await update.message.reply_text(f"⏳ Загружаю {topic} roadmap...")
    
    image_url = await get_roadmap_image(topic)
    
    if image_url:
        try:
            await update.message.reply_photo(
                photo=image_url,
                caption=f"🗺 Дорожная карта: {topic.capitalize()}\n\nСсылка: {ROADMAP_BASE_URL}{topic}"
            )
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=loading_msg.message_id
            )
        except Exception as e:
            logger.error(f"Send error: {e}")
            await update.message.reply_text("⚠️ Ошибка при отправке")
    else:
        await update.message.reply_text(
            f"⚠️ Не удалось загрузить карту. Попробуйте позже или посетите:\n{ROADMAP_BASE_URL}{topic}"
        )

async def map_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /map"""
    if not context.args:
        await update.message.reply_text("ℹ️ Используйте: /map <направление>\nПример: /map frontend")
        return
    
    topic = context.args[0].lower()
    await handle_roadmap(update, context, topic)

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل النصية"""
    topic = update.message.text.lower().strip()
    await handle_roadmap(update, context, topic)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("map", map_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
    
    app.add_error_handler(lambda update, context: logger.error(f"Error: {context.error}"))
    
    logger.info("Бот успешно запущен!")
    app.run_polling()
