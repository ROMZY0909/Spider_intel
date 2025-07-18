# app/telegram/webhook.py

from fastapi import APIRouter, Request, HTTPException
import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

TELEGRAM_SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

@router.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()

        # 🔒 Vérification du token secret (optionnelle mais recommandée)
        if TELEGRAM_SECRET_TOKEN:
            header_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
            if header_token != TELEGRAM_SECRET_TOKEN:
                raise HTTPException(status_code=403, detail="Invalid secret token")

        logging.info(f"📨 Message reçu de Telegram : {update}")

        # 💬 Répondre automatiquement au message reçu
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")

        if chat_id and text:
            reply_text = f"🤖 SPIDER INTEL a bien reçu ton message : '{text}'"
            response = requests.post(TELEGRAM_API_URL, json={
                "chat_id": chat_id,
                "text": reply_text
            })

            if response.status_code != 200:
                logging.error(f"⚠️ Erreur lors de l'envoi de message : {response.text}")

        return {"ok": True}

    except Exception as e:
        logging.error(f"❌ Erreur dans le webhook : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
    