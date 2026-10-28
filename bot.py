import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import init_db, add_task

# BotFather'dan olgan tokeningizni qo'shtirnoq ichiga yozasiz
TOKEN = "SIZNING_TELEGRAM_BOT_TOKENINGIZ"

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Salom! Men sizning shaxsiy yordamchingizman. Menga vazifangizni yozib yuboring.")

@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    user_id = message.from_user.id
    
    add_task(user_id, user_text, "Ertaga")
    await message.answer(f"✅ Vazifa qabul qilindi va bazaga saqlandi:\n👉 {user_text}")

async def main():
    init_db()
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())