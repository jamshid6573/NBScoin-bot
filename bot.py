import asyncio
import logging
from aiogram import Bot, Dispatcher
from app import rt, CheckAdminAndBanMiddleware, BanCallbackMiddleware
from database import Database
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
db = Database()

dp.message.middleware(CheckAdminAndBanMiddleware())
dp.callback_query.middleware(BanCallbackMiddleware())


async def main():
    dp.include_router(rt)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        print("Bot Start")
        asyncio.run(main())
    except KeyboardInterrupt:
        db.close()
        print("Exit")