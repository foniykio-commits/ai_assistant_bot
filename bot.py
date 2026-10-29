import asyncio
import os
import re
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# 1. Render talab qiladigan minimal port-server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    # Render avtomatik beradigan PORT ni oladi, bo'lmasa 10000 ni ishlatadi
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Serverni fonda alohida ipda (thread) ishga tushirish
threading.Thread(target=run_server, daemon=True).start()

# 2. Telegram Bot va Gemini qismi
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = "AQ.Ab8RN6IUHn7h_GeSchw3k52dHS_NuulF7n_xCMw6j9QClt6IjQ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Men Gemini AI bilan ishlaydigan aqlli yordamchingizman. 🚀\n\n"
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
    """

    try:
        response = model.generate_content(prompt)
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
            await message.answer("Vaqtni aniqlay olmadim. Iltimos, vaqtni aniqroq yozib ko'ring.")
            
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
