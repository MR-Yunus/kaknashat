from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests
import logging

# إعدادات البوت
TELEGRAM_TOKEN = '8183870944:AAGftaeglixiUoop3u9xAKQWcBYcULbtzzk'
ROADMAP_BASE_URL = "https://roadmap.sh/pdfs/roadmaps/"

# القائمة الكاملة للمجالات المتاحة
AVAILABLE_ROADMAPS = {
    'absolute beginners': 'beginners.pdf',
    'web development': 'web-development.pdf',
    'frameworks': 'frameworks.pdf',
    'languages': 'languages-platforms.pdf',
    'devops': 'devops.pdf',
    'mobile': 'mobile-development.pdf',
    'databases': 'databases.pdf',
    'computer science': 'computer-science.pdf',
    'machine learning': 'machine-learning.pdf',
    'management': 'management.pdf',
    'game development': 'game-development.pdf',
    'design': 'design.pdf',
    'blockchain': 'blockchain.pdf',
    'cyber security': 'cyber-security.pdf',
    'frontend': 'frontend.pdf',
    'backend': 'backend.pdf',
    'full stack': 'full-stack.pdf',
    'api design': 'api-design.pdf',
    'qa': 'qa.pdf',
    'android': 'android.pdf',
    'ios': 'ios.pdf',
    'postgresql': 'postgresql.pdf',
    'software architect': 'software-architect.pdf',
    'technical writer': 'technical-writer.pdf',
    'devrel': 'devrel-engineer.pdf',
    'ai': 'ai-data-scientist.pdf',
    'ai engineer': 'ai-engineer.pdf',
    'ai agents': 'ai-agents.pdf',
    'data analyst': 'data-analyst.pdf',
    'mlops': 'mlops.pdf',
    'product manager': 'product-manager.pdf',
    'engineering manager': 'engineering-manager.pdf',
    'game dev': 'client-side-game-development.pdf',
    'server game dev': 'server-side-game-development.pdf',
    'ux design': 'ux-design.pdf',
    'graphql': 'graphql.pdf',
    'git': 'git-github.pdf',
    'react': 'react.pdf',
    'vue': 'vue.pdf',
    'angular': 'angular.pdf',
    'spring boot': 'spring-boot.pdf',
    'asp.net': 'aspnet-core.pdf',
    'javascript': 'javascript.pdf',
    'typescript': 'typescript.pdf',
    'node.js': 'nodejs.pdf',
    'php': 'php.pdf',
    'c++': 'cpp.pdf',
    'go': 'go.pdf',
    'rust': 'rust.pdf',
    'python': 'python.pdf',
    'java': 'java.pdf',
    'sql': 'sql.pdf',
    'docker': 'docker.pdf',
    'kubernetes': 'kubernetes.pdf',
    'aws': 'aws.pdf',
    'cloudflare': 'cloudflare.pdf',
    'linux': 'linux.pdf',
    'terraform': 'terraform.pdf',
    'react native': 'react-native.pdf',
    'flutter': 'flutter.pdf',
    'mongodb': 'mongodb.pdf',
    'redis': 'redis.pdf',
    'data structures': 'data-structures.pdf',
    'system design': 'system-design.pdf',
    'design architecture': 'design-and-architecture.pdf',
    'code review': 'code-review.pdf',
    'ai red teaming': 'ai-red-teaming.pdf',
    'prompt engineering': 'prompt-engineering.pdf',
    'design system': 'design-system.pdf'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /start"""
    categories = "\n".join([
        "📌 Основные категории:",
        "• web development • devops • mobile • databases",
        "• computer science • machine learning • design",
        "",
        "👨‍💻 Ролевые дорожные карты:",
        "• frontend • backend • full stack • qa",
        "• android • ios • software architect",
        "",
        "🛠 Навыки/технологии:",
        "• react • vue • angular • javascript • python",
        "• java • docker • kubernetes • aws • linux",
        "",
        "ℹ️ Полный список: /list"
    ])
    
    await update.message.reply_text(
        f"📚 Добро пожаловать в бот дорожных карт!\n\n{categories}\n\n"
        "Просто напишите название технологии или роли"
    )

async def list_roadmaps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إرسال قائمة كاملة بالمجالات"""
    roadmaps_list = "\n".join([f"• {k}" for k in sorted(AVAILABLE_ROADMAPS.keys())])
    await update.message.reply_text(
        "📋 Доступные дорожные карты:\n\n" + roadmaps_list +
        "\n\nℹ️ Можно использовать как английские, так и русские названия"
    )

async def send_roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE, topic: str):
    """إرسال ملف PDF"""
    normalized_topic = topic.lower().strip()
    
    # البحث عن أفضل تطابق
    matched_topic = None
    for roadmap in AVAILABLE_ROADMAPS:
        if normalized_topic in roadmap or roadmap in normalized_topic:
            matched_topic = roadmap
            break
    
    if not matched_topic:
        await update.message.reply_text(
            "❌ Не найдено дорожной карты для этого запроса.\n"
            "Попробуйте /list для просмотра доступных вариантов"
        )
        return

    pdf_url = ROADMAP_BASE_URL + AVAILABLE_ROADMAPS[matched_topic]
    
    try:
        # التحقق من وجود الملف
        response = requests.head(pdf_url)
        if response.status_code != 200:
            await update.message.reply_text(
                f"⚠️ Файл временно недоступен. Попробуйте позже.\n"
                f"Или посетите: {pdf_url}"
            )
            return
            
        await update.message.reply_document(
            document=pdf_url,
            caption=f"📄 Дорожная карта: {matched_topic.capitalize()}"
        )
    except Exception as e:
        logging.error(f"Error sending PDF: {e}")
        await update.message.reply_text(
            "⚠️ Произошла ошибка при загрузке файла. Попробуйте позже."
        )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل النصية"""
    topic = update.message.text
    await send_roadmap(update, context, topic)

async def map_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /map"""
    if not context.args:
        await update.message.reply_text("ℹ️ Использование: /map <название технологии>\nПример: /map react")
        return
    
    topic = " ".join(context.args)
    await send_roadmap(update, context, topic)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_roadmaps))
    app.add_handler(CommandHandler("map", map_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    logging.info("Бот запущен и готов к работе!")
    app.run_polling()
