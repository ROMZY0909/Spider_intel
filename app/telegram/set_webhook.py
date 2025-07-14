# app/telegram/set_webhook.py

import os
import asyncio
import telegram
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")

if not TOKEN or not WEBHOOK_URL:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN ou TELEGRAM_WEBHOOK_URL est manquant dans le .env")

bot = telegram.Bot(token=TOKEN)

async def set_webhook():
    success = await bot.set_webhook(url=WEBHOOK_URL)
    if success:
        print(f"✅ Webhook Telegram défini avec succès sur : {WEBHOOK_URL}")
    else:
        print("❌ Échec lors de la définition du webhook.")

if __name__ == "__main__":
    asyncio.run(set_webhook())
