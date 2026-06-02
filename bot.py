import os
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from rapidfuzz import process, fuzz

# =========================
# LOGGING
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# =========================
# TOKEN (من Environment Variables)
# =========================

TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")

# =========================
# DATA BASE
# =========================

QUESTIONS = {
    "بنود التقسيط المتاح": {
        "keywords": ["تقسيط", "اقساط", "بنك مصر", "cib", "قسط","مصر","تقسيط اهلى", "تقسيط cib"],
        "answer": (
            "• تقسيط بنك اهلي لمدة 6 شهور بدون فوائد\n"
            "• تقسيط بنك CIB لمدة 6 شهور بدون فوائد\n"
            "• تقسيط بنك مصر لمدة 3 شهور بدون فوائد"
        ),
        "photo": None
    },

    "خصم موظفي البنك الاهلي": {
        "keywords": ["بنك اهلي", "اهلي", "الاهلي", "خصم موظفين اهلي"],
        "answer": "الخصم ساري حتى 28-10-2026",
        "photo": "images/خصم بنك اهلى.jpg"
    },

    "خصم بابلو": {
        "keywords": ["بابلو", "pablo", "مطعم بابلو"],
        "answer": "ساري حتي 31-12-2026",
        "photo": "images/خصم بابلو.jpg"
    },

    "خصم رئاسة الجمهورية": {
        "keywords": ["رئاسة", "خصم الرئاسة", " رئاسة الجمهورية"],
        "answer": "كروت عام 2025 الصرف حتى 30-6-2026 بدون تطبيق خصم\nكروت عام 2026 يطبق خصم 10% ساري حتى 30-6-2027",
        "photo": "images/رئاسة الجمهورية.jpg"
    },

    "خصم نقابة المهن الطبية": {
        "keywords": ["اطباء", "خصم اطباء", "دكتور"],
        "answer": "ساري حتي 28-2-2027",
        "photo": "images/خصم الاطباء.jpg"
    },

    "خصم نقابة المهندسين": {
        "keywords": ["مهندس", "مهندسين", "خصم المهندسين"],
        "answer": "ساري حتي 31-12-2026",
        "photo": "images/خصم مهندسين.jpg"
    },

    "خصم كويك": {
        "keywords": ["كويك", "خصم كويك ","Quik Discount"],
        "answer": "ساري",
        "photo": "images/Quik Discount.jpg"
    },

    "خصم مصلحة الضرائب": {
        "keywords": ["ضرائب", "خصم الضرائب", "مصلحة الضرائب"],
        "answer": "ساري حتي 31-12-2026",
        "photo": "images/خصم الضرائب.jpg"
    },

    "خصم موظفين شركة ارامكس": {
        "keywords": ["ارامكس", "موظفين ارامكس", "خصم شركة ارامكس"],
        "answer": "الخصم ساري حتي 31-12-2026",
        "photo": "images/خصم ارامكس.jpg"
    },

    }

# =========================
# HELP MESSAGE
# =========================

HELP_TEXT = """
📌 اكتب أي كلمة من التالي:

- تقسيط
- بنك اهلي
- بنك مصر
- بابلو
- مهندسين

💡 أو اكتب جملة كاملة مثل:
"عايز تقسيط بنك مصر"
"""

# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك 👋\n"
        "اكتب سؤالك وسأساعدك فورًا."
    )

# =========================
# HELP COMMAND
# =========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)

# =========================
# SMART SEARCH ENGINE
# =========================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    best_match = None
    best_score = 0

    # 1- Keyword matching (الأقوى)
    for key, data in QUESTIONS.items():

        for kw in data.get("keywords", []):

            if kw.lower() in text:
                best_match = key
                best_score = 100
                break

        if best_score == 100:
            break

    # 2- Fuzzy fallback
    if not best_match:

        result = process.extractOne(
            text,
            QUESTIONS.keys(),
            scorer=fuzz.WRatio
        )

        if result:
            best_match, best_score = result[0], result[1]

    # 3- Reply
    if best_match and best_score >= 60:

        item = QUESTIONS[best_match]

        answer = item["answer"]
        photo = item.get("photo")

        if photo and os.path.exists(photo):
            with open(photo, "rb") as img:
                await update.message.reply_photo(photo=img, caption=answer)
        else:
            await update.message.reply_text(answer)

    else:
        await update.message.reply_text(HELP_TEXT)

# =========================
# ERROR HANDLER
# =========================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Error occurred:", exc_info=context.error)

# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Messages
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )

    # Errors
    app.add_error_handler(error_handler)

    print("✅ Bot is running...")

    app.run_polling()

# =========================

if __name__ == "__main__":
    main()
