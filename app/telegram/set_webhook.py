# app/telegram/set_webhook.py

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

try:
    from telegram import Bot
except ImportError:
    raise ImportError("❌ Le module 'telegram' est introuvable. Vérifie que 'python-telegram-bot' est bien installé.")

# Récupération des variables d'environnement
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")

if not TOKEN or not WEBHOOK_URL:
    raise EnvironmentError("❌ Variables TELEGRAM_BOT_TOKEN ou TELEGRAM_WEBHOOK_URL manquantes dans .env")

bot = Bot(token=TOKEN)

async def set_webhook():
    try:
        success = await bot.set_webhook(url=WEBHOOK_URL)
        if success:
            print(f"✅ Webhook Telegram défini avec succès : {WEBHOOK_URL}")
        else:
            print("⚠️ Le webhook a été défini mais n’a pas retourné de succès explicite.")
    except Exception as e:
        print(f"❌ Erreur lors de la définition du webhook : {e}")

if __name__ == "__main__":
    asyncio.run(set_webhook())
