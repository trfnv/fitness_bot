from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.keyboards import get_gender_keyboard

router = Router()

class UserData(StatesGroup):
    gender = State()
    age = State()
    level = State()
    program = State()  # Сохранение выбранной программы
    schedule_days = State()  # Дни недели
    schedule_time = State()  # Время тренировок

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "👋 Привет! Я помогу подобрать программу тренировок.\n"
        "Выбери свой пол:",
        reply_markup=get_gender_keyboard()
    )
    await state.set_state(UserData.gender)

@router.message(UserData.gender)
async def process_gender(message: types.Message, state: FSMContext):
    gender = message.text.lower()
    if gender not in ["мужчина", "женщина"]:
        await message.answer("Пожалуйста, выбери пол с помощью кнопок.")
        return

    await state.update_data(gender="male" if gender == "мужчина" else "female")
    await message.answer(
        "Введи свой возраст цифрами (например, 25):",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(UserData.age)