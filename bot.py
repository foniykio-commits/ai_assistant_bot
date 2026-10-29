import asyncio
import os
import re
from mistralai import Mistral
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Telegram va Mistral kalitlari
BOT_TOKEN = os.getenv("BOT_TOKEN")
MISTRAL_API_KEY = "Mstrl_mSymMNOhOyltpvSuc7M88rfAmfY8QSDb_1lFu07"
model_name = "mistral-small-latest"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Mistral mijozini sozlash
client = Mistral(api_key=MISTRAL_API_KEY)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Men Mistral AI bilan ishlaydigan aqlli yordamchingizman. 🚀\n\n"
        "Menga ixtiyoriy shaklda vaqt va eslatmani yozing, masalan:\n"
        "• 'Yarim soatdan keyin choy ichishni eslat'\n"
        "• '1 soat 15 minutdan keyin darsni boshla deb ayt'"
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
        response = client.chat.complete(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        ai_out = response.choices[0].message.content.strip()
        
        sec_match = re.search(r'SEKUND:\s*(\d+)', ai_out)
        msg_match = re.search(r'XABAR:\s*(.+)', ai_out)
        
        if sec_match:
            seconds = int(sec_match.group(1))
            note = msg_match.group(1).strip() if msg_match else "Eslatilgan vaqt bo'ldi!"
            
            minutes = seconds // 60
            sec_rem = seconds % 60
            time_str = f"{minutes} minut " if minutes > 0 else ""
            time_str += f"{sec_rem} sekund" if sec_rem > 0 else ""
            
            await message.answer(f"Tushundim! ⏳ **{time_str.strip()}**dan keyin eslataman.")
            
            await asyncio.sleep(seconds)
            await message.answer(f"🔔 **Eslatma:** {note}")
        else:
            await message.answer("Vaqtni aniqlay olmadim. Iltimos, vaqtni aniqroq yozib ko'ring.")
            
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
