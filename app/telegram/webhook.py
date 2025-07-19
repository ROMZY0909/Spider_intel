# app/telegram/webhook.py

from fastapi import APIRouter, Request
import os
from dotenv import load_dotenv
from telegram import Bot, Update

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

        update = Update.de_json(data, bot)

        if update.message:
            chat_id = update.message.chat.id
            message_text = update.message.text.strip()

            if message_text == "/start":
                bot.send_message(
                    chat_id=chat_id,
                    text="🕷️ Bienvenue sur SPIDER INTEL ! Je suis prêt à scanner pour toi."
                )

            elif message_text.startswith("/scan"):
                try:
                    ip = message_text.split()[1]
                    from utils.scanner_core import full_osint_lookup
                    result = full_osint_lookup(ip)

                    country = result.get("ip-api", {}).get("country", "N/A")
                    abuse_score = result.get("abuseipdb", {}).get("abuseConfidenceScore", "N/A")
                    org = result.get("shodan", {}).get("org", "N/A")

                    response = (
                        f"🕷️ Résultat du scan pour l'IP : {ip}\n\n"
                        f"🌍 Pays : {country}\n"
                        f"👮 Score AbuseIPDB : {abuse_score}\n"
                        f"🏢 Fournisseur : {org}"
                    )
                    bot.send_message(chat_id=chat_id, text=response)

                except Exception as scan_error:
                    bot.send_message(chat_id=chat_id, text=f"❌ Erreur pendant le scan : {scan_error}")

            else:
                bot.send_message(
                    chat_id=chat_id,
                    text=f"🔎 Tu as dit : {message_text}"
                )

        return {"status": "ok"}

    except Exception as e:
        print(f"❌ Erreur dans le webhook Telegram : {e}")
        return {"status": "error", "detail": str(e)}
