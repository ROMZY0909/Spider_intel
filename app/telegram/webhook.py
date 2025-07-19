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
                    text="🕷️ Bienvenue sur SPIDER INTEL !\nJe suis prêt à scanner pour toi.\n\nUtilise la commande :\n`/scan 8.8.8.8`",
                    parse_mode="Markdown"
                )

            elif message_text.startswith("/scan"):
                try:
                    ip = message_text.split()[1]

                    # Import ici pour éviter l'erreur au chargement Render
                    from scanner.email_scanner import scan_email

                    result = scan_email(ip)
                    summary = result.get("summary", "❌ Résumé indisponible.")

                    bot.send_message(
                        chat_id=chat_id,
                        text=f"🔍 Résultat du scan pour *{ip}* :\n\n{summary}",
                        parse_mode="Markdown"
                    )

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
