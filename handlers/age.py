from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from handlers.start import UserData
from utils.keyboards import get_level_keyboard

router = Router()

@router.message(UserData.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введи возраст цифрами (например, 25).")
        return

    if age < 20 or age > 39:
        await message.answer("Программы доступны для возраста 20–39 лет. Введи возраст еще раз.")
        return

    age_group = "20s" if age < 30 else "30s"
    await state.update_data(age_group=age_group)
    await message.answer(
        "Выбери уровень подготовки:",
        reply_markup=get_level_keyboard()
    )
    await state.set_state(UserData.level)
