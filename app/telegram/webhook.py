# app/telegram/webhook.py

from fastapi import APIRouter, Request
import os
from app.telegram._patched_inputfile import InputFile
from dotenv import load_dotenv

# ✅ Imports nécessaires depuis python-telegram-bot
from telegram import Bot, Update
from telegram.constants import ParseMode

# Chargement des variables d'environnement
load_dotenv()

# Initialisation du bot Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)

# Déclaration du routeur FastAPI
router = APIRouter()

@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        print("✅ Message reçu depuis Telegram :", data)

        # ✅ Conversion en objet Update
        update = Update.de_json(data, bot)

        # Traitement du message reçu
        if update.message:
            chat_id = update.message.chat.id
            message_text = update.message.text

            # Exemple de réponse automatique
            if message_text == "/start":
                bot.send_message(
                    chat_id=chat_id,
                    text="🕷️ Bienvenue sur SPIDER INTEL !\nJe suis prêt à scanner pour toi.",
                    parse_mode=ParseMode.HTML
                )
            else:
                bot.send_message(
                    chat_id=chat_id,
                    text=f"🔎 Tu as dit : {message_text}",
                    parse_mode=ParseMode.HTML
                )

        return {"status": "ok"}

    except Exception as e:
        print(f"❌ Erreur dans le webhook Telegram : {e}")
        return {"status": "error", "detail": str(e)}
