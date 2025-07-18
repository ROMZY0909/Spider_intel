# app/telegram/webhook.py

from fastapi import APIRouter, Request, HTTPException
import os
from dotenv import load_dotenv
import logging

load_dotenv()

router = APIRouter()

TELEGRAM_SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN")  # Optionnel mais recommandé

@router.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        # 🔒 Optionnel : vérification d’un token secret si configuré
        if TELEGRAM_SECRET_TOKEN:
            header_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
            if header_token != TELEGRAM_SECRET_TOKEN:
                raise HTTPException(status_code=403, detail="Invalid secret token")

        # 📌 Tu peux ici traiter l’update
        logging.info(f"📨 Message reçu de Telegram : {update}")
        return {"ok": True}
    except Exception as e:
        logging.error(f"❌ Erreur dans le webhook : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
