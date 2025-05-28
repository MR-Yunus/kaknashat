import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN", "7233502689:AAHE6-fs31OuuXdXd_1jvAv-TaNLGwRbidE")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Напиши /ai чтобы получить дорожную карту ИИ.")

async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://roadmap.sh/ai"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all("h2")

    message = "📘 Основные шаги для изучения ИИ:\n"
    for i, item in enumerate(items[:10], 1):
        message += f"{i}. {item.text.strip()}\n"
    await update.message.reply_text(message)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ai", ai))
    print("✅ Бот работает...")
    app.run_polling()
