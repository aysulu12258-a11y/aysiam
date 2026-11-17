import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from database import init_db
from handlers.admin import admin_handler
from handlers.user_handlers import user_handler
from dotenv import load_dotenv

load_dotenv()



BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set. Example: set BOT_TOKEN=your_token_here")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

init_db()

dp.include_router(admin_handler)
dp.include_router(user_handler)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
