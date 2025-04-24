from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from handlers.start import UserData
from aiogram import Bot

# Функция для отправки напоминаний
async def send_reminder(bot: Bot, chat_id: int, message: str):
    """
    Отправляет напоминание пользователю.

    :param bot: Экземпляр бота.
    :param chat_id: ID чата пользователя.
    :param message: Текст напоминания.
    """
    await bot.send_message(chat_id=chat_id, text=message)

router = Router()

# Клавиатура для выбора дней недели
def get_days_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            ["Пн, Ср, Пт"],
            ["Вт, Чт"],
            ["Сб, Вс"],
            ["Другое..."]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

@router.message(UserData.program)
async def ask_schedule_days(message: types.Message, state: FSMContext):
    await message.answer(
        "📅 Выбери дни тренировок:",
        reply_markup=get_days_keyboard()
    )
    await state.set_state(UserData.schedule_days)

@router.message(UserData.schedule_days)
async def ask_schedule_time(message: types.Message, state: FSMContext):
    days = message.text
    await state.update_data(schedule_days=days)
    await message.answer(
        "⏰ Введи время тренировок (например, 18:00):",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(UserData.schedule_time)

@router.message(UserData.schedule_time)
async def confirm_schedule(message: types.Message, state: FSMContext):
    time = message.text
    await state.update_data(schedule_time=time)
    user_data = await state.get_data()

    # Формируем итоговое сообщение
    response = (
        "✅ Отлично! Твой план готов:\n\n"
        f"🏋️ **Программа:** {user_data['program']['title']}\n"
        f"📅 **Дни:** {user_data['schedule_days']}\n"
        f"⏰ **Время:** {user_data['schedule_time']}\n\n"
        "Я буду присылать напоминания!"
    )
    await message.answer(response)
    await state.clear()

    # Здесь можно добавить логику напоминаний (например, через APScheduler)