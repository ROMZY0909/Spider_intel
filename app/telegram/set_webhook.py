# app/telegram/set_webhook.py

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

try:
    from telegram import Bot
except ImportError:
    raise ImportError("❌ Le module 'telegram' est introuvable. Installe-le avec : pip install python-telegram-bot==20.7")

# Chargement des variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = os.getenv("BASE_WEBHOOK_URL")  # Ex: https://spider-intel.onrender.com
SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN")  # Facultatif

# Vérification stricte
if not TOKEN or not BASE_URL:
    raise EnvironmentError("❌ Variables TELEGRAM_BOT_TOKEN ou BASE_WEBHOOK_URL manquantes dans .env")

# Définition du chemin exact du webhook
WEBHOOK_PATH = os.getenv("TELEGRAM_WEBHOOK_PATH", "/telegram/webhook")
FULL_WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)

async def set_webhook():
    try:
        success = await bot.set_webhook(
            url=FULL_WEBHOOK_URL,
            secret_token=SECRET_TOKEN if SECRET_TOKEN else None
        )
        if success:
            print(f"✅ Webhook Telegram défini avec succès : {FULL_WEBHOOK_URL}")
        else:
            print("⚠️ Le webhook a été défini mais n’a pas retourné de succès explicite.")
    except Exception as e:
        print(f"❌ Erreur lors de la définition du webhook : {e}")

if __name__ == "__main__":
    asyncio.run(set_webhook())
