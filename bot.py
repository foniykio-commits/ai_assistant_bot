import asyncio
import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from google import genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = "AQ.Ab8RN6IUHn7h_GeSchw3k52dHS_NuulF7n_xCMw6j9QClt6IjQ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Gemini mijozini yaratish
client = genai.Client(api_key=GEMINI_KEY)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Men Gemini AI bilan ishlaydigan aqlli yordamchingizman. 🚀\n\n"
        "Menga ixtiyoriy shaklda vaqt va eslatmani yozing, masalan:\n"
        "• 'Yarim soatdan keyin choy ichishni eslat'\n"
        "• '1 soat 15 minutdan keyin darsni boshla deb ayt'\n"
        "• '45 sekunddan keyin xabar ber'"
    )

@dp.message()
async def ai_reminder_handler(message: types.Message):
    user_text = message.text
    
    prompt = f"""
    Senga foydalanuvchi quyidagi matnni yozdi: "{user_text}"
    Sening vazifang ushbu matndan foydalanuvchi qancha VAQT (sekundlarda) kutmoqchi ekanligini va qanday ESLATMA xabari qoldirganini aniqlash.
    
    Javobni FAQAT VA FAQAT mana bu formatda ber, hech qanday ortiqcha so'z yozma:
    SEKUND: [Jami sekundlar soni faqat raqamda]
    XABAR: [Eslatma matni]

    Misol uchun:
    Input: "yarim soatdan keyin kitob o'qishni eslat"
    Output:
    SEKUND: 1800
    XABAR: Kitob o'qish vaqti bo'ldi!
    """

    try:
        # Eng barqaror model nomidan foydalanamiz
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
        )
        ai_out = response.text.strip()
        
        sec_match = re.search(r'SEKUND:\s*(\d+)', ai_out)
        msg_match = re.search(r'XABAR:\s*(.+)', ai_out)
        
        if sec_match:
            seconds = int(sec_match.group(1))
            note = msg_match.group(1).strip() if msg_match else "Eslatilgan vaqt bo'ldi!"
            
            minutes = seconds // 60
            sec_rem = seconds % 60
            time_str = f"{minutes} minut " if minutes > 0 else ""
            time_str += f"{sec_rem} sekund" if sec_rem > 0 else ""
            
            await message.answer(f"Tushundim! ⏳ {time_str.strip()}dan keyin eslataman.")
            
            await asyncio.sleep(seconds)
            await message.answer(f"🔔 Eslatma: {note}")
        else:
            await message.answer(f"AI javobidan vaqtni o'qib bo'lmadi. AI javobi: {ai_out}")
            
    except Exception as e:
        # Endi xatolikning aniq sababini Telegramga yozib yuboradi
        await message.answer(f"ANIQ XATOLIK: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
