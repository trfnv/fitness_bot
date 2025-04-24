import re
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from handlers.start import UserData
from utils.program_picker import get_program

router = Router()

def escape_markdown(text: str) -> str:
    """Экранирует специальные символы для MarkdownV2"""
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return ''.join(['\\' + char if char in escape_chars else char for char in text])

@router.message(UserData.level)
async def process_level(message: Message, state: FSMContext):
    level = message.text.lower()

    if level not in ["начинающий", "продвинутый"]:
        await message.answer("Пожалуйста, выбери уровень с помощью кнопок.")
        return

    level_group = "beginner" if level == "начинающий" else "advanced"
    user_data = await state.get_data()

    program = get_program(
        gender=user_data["gender"],
        age_group=user_data["age_group"],
        level=level_group
    )

    if not program:
        await message.answer("❌ Программа не найдена. Попробуй другие параметры.")
        return

    await state.update_data(program=program)

    title = escape_markdown(program.get("title", "Программа"))
    description = escape_markdown(program.get("description", ""))
    duration = escape_markdown(str(program.get("duration_weeks", "")))

    response = f"🏋️ *{title}*\n"
    response += f"📝 {description}\n"
    response += f"⏳ Продолжительность: {duration} недель\n\n"

    # Добавляем отформатированные секции
    for section_content in program.get("sections", {}).values():
        response += f"{escape_markdown(section_content)}\n\n"

    await message.answer(response, parse_mode="MarkdownV2")
    await state.set_state(UserData.program)
