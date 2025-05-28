from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

TELEGRAM_TOKEN = '7511979228:AAGu0Qoi4Ejny_sLVbRsa4yyLzO6mtXCuOA'
SCREENSHOT_API_KEY = 'XQY7QG6-R5M4M5P-HMQGWAV-QKDZCJB'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне область, например: frontend, devops, ai и я пришлю карту 📌")

async def roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши название области, например: frontend")
        return

    topic = context.args[0].lower()
    url = f"https://roadmap.sh/{topic}"
    screenshot_url = f"https://api.screenshotapi.net/screenshot?token={SCREENSHOT_API_KEY}&url={url}&output=image&file_type=png"

    await update.message.reply_photo(photo=screenshot_url, caption=f"🗺️ Дорожная карта для: {topic}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('map', roadmap))
    app.run_polling()
