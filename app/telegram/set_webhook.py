# app/telegram/set_webhook.py

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

try:
    from telegram import Bot
except ImportError:
    raise ImportError("❌ Le module 'telegram' est introuvable. Installe-le avec : pip install python-telegram-bot==20.7")

# ✅ Chargement des variables d’environnement
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")
SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN")  # recommandé

if not TOKEN or not WEBHOOK_URL:
    raise EnvironmentError("❌ Variables TELEGRAM_BOT_TOKEN ou BASE_WEBHOOK_URL manquantes dans .env")

bot = Bot(token=TOKEN)

async def set_webhook():
    try:
        full_url = f"{WEBHOOK_URL}/webhook"
        success = await bot.set_webhook(
            url=full_url,
            secret_token=SECRET_TOKEN if SECRET_TOKEN else None
        )
        if success:
            print(f"✅ Webhook Telegram défini avec succès : {full_url}")
        else:
            print("⚠️ Le webhook a été défini mais n’a pas retourné de succès explicite.")
    except Exception as e:
        print(f"❌ Erreur lors de la définition du webhook : {e}")

if __name__ == "__main__":
    asyncio.run(set_webhook())
