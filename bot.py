import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import start, age, level
from handlers.schedule import send_reminder

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация роутеров
dp.include_router(start.router)
dp.include_router(age.router)
dp.include_router(level.router)

async def main():
    try:
        # Запуск бота с обработкой ошибок
        logger.info("Bot is starting...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Error occurred during bot execution: {e}")
