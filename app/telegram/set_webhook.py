# app/telegram/set_webhook.py

import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = os.getenv("BASE_WEBHOOK_URL")
WEBHOOK_PATH = os.getenv("TELEGRAM_WEBHOOK_PATH", "/telegram/webhook")
SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN")

if not TOKEN or not BASE_URL:
    raise EnvironmentError("❌ Variables TELEGRAM_BOT_TOKEN ou BASE_WEBHOOK_URL manquantes dans .env")

FULL_WEBHOOK_URL = f"{BASE_URL.rstrip('/')}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)

def set_webhook():
    try:
        success = bot.set_webhook(
            url=FULL_WEBHOOK_URL,
            secret_token=SECRET_TOKEN if SECRET_TOKEN else None
        )
        if success:
            print(f"✅ Webhook Telegram défini avec succès : {FULL_WEBHOOK_URL}")
        else:
            print("⚠️ Webhook défini mais sans retour explicite de succès.")
    except Exception as e:
        print(f"❌ Erreur lors de la définition du webhook : {e}")

if __name__ == "__main__":
    set_webhook()
