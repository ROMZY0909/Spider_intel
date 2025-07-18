# app/telegram/set_webhook.py

import os
from dotenv import load_dotenv
from telegram import Bot

# Chargement des variables d'environnement
load_dotenv()

# Récupération des variables nécessaires
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")

# Vérification des variables
if not TOKEN or not WEBHOOK_URL:
    raise EnvironmentError("❌ Variables TELEGRAM_BOT_TOKEN ou TELEGRAM_WEBHOOK_URL manquantes dans le fichier .env")

# Initialisation du bot
bot = Bot(token=TOKEN)

def set_webhook():
    try:
        success = bot.set_webhook(url=WEBHOOK_URL)
        if success:
            print(f"✅ Webhook Telegram défini avec succès : {WEBHOOK_URL}")
        else:
            print("⚠️ Le webhook a été défini mais sans retour de succès explicite.")
    except Exception as e:
        print(f"❌ Erreur lors de la définition du webhook : {e}")

# Exécution directe
if __name__ == "__main__":
    set_webhook()
