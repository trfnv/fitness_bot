import json
from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_user

def load_program(program_id):
    with open("data/programs.json", "r", encoding="utf-8") as f:
        programs = json.load(f)
    return programs.get(program_id)

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    
    if not user:
        await update.message.reply_text("Сначала зарегистрируйтесь с помощью команды /start.")
        return

    program_id = user[5]  # program_id stored in 6-й колонке
    program = load_program(program_id)

    if not program:
        await update.message.reply_text("Не удалось загрузить вашу программу тренировок.")
        return

    text = f"🏋️‍♂️ *{program['title']}*\n_{program['description']}_\n\n"
    for section, exercises in program["plan"].items():
        emoji = {
            "warmup": "🔥 Разминка",
            "cardio": "🏃 Кардио",
            "strength": "💪 Сила",
            "stretch": "🧘 Растяжка"
        }.get(section, section.capitalize())
        text += f"*{emoji}:*\n" + "\n".join(f"• {ex}" for ex in exercises) + "\n\n"

    await update.message.reply_text(text, parse_mode="Markdown")
