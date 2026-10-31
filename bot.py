import os
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# ==========================================
# TOKEN VA TELEGRAM ID TO'G'RIDAN-TO'G'RI YOZILDI
# ==========================================
BOT_TOKEN = "9218041811:AAEmRJclca1OLgWaLmGi5qr4WK2JhXbwfrU"
MY_CHAT_ID = "6194723145"  # Sizning Telegram ID raqamingiz to'g'ridan-to'g'ri ulandi

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==========================================
# 5 MINUTLIK TAYMER (Background Task)
# ==========================================
async def five_minute_scheduler():
    """Har 5 minutda avtomatik ravishda eslatma yuboradigan funksiya"""
    while True:
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            
            if MY_CHAT_ID:
                await bot.send_message(
                    chat_id=int(MY_CHAT_ID),
                    text=f"⏰ **Vaqt eslatmasi:** Hozir soat **{current_time}**.\n"
                         f"5 daqiqalik interval keldi. Joriy vazifa va 30 daqiqalik zadishkalarni tekshiring!"
                )
        except Exception as e:
            print(f"Eslatma yuborishda xatolik: {e}")
        
        # 5 minut (300 sekund) kutish
        await asyncio.sleep(5 * 60)

# ==========================================
# HANDLERLAR
# ==========================================
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! @javloinbek_yordamchi_bot muvaffaqiyatli ishga tushdi.\n"
        "Har 5 minutda avtomatik ravishda vaqt eslatmalari yuborish tizimi faol va sizga ulangan!"
    )

@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"Qabul qilindi: {message.text}")

# ==========================================
# RENDER UCHUN WEB SERVER
# ==========================================
async def handle_ping(request):
    return web.Response(text="Bot is running active!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/ping", handle_ping)
    
    port = int(os.getenv("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# ==========================================
# MAIN
# ==========================================
async def main():
    await start_web_server()
    asyncio.create_task(five_minute_scheduler())
    print("🤖 Bot polling rejimida ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
