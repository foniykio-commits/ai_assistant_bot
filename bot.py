import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Loglarni yoqish (xatoliklarni ko'rib turish uchun)
logging.basicConfig(level=logging.INFO)

# Tokenni Render'dagi Environment (BOT_TOKEN) dan avtomatik oladi
TOKEN = os.getenv("BOT_TOKEN")

# Bot va Dispatcher yaratish
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Schedulerni sozlash (24/7 rejim va vaqtli vazifalar uchun)
scheduler = AsyncIOScheduler()

# /start buyrug'i kelganda ishlaydigan funksiya
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Botingiz muvaffaqiyatli ishga tushdi va 24/7 rejimida ishlamoqda. 🚀")

# Botni ishga tushiruvchi asosiy qism
async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
