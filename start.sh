#!/bin/bash
# Démarrer FastAPI via Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 10000 &

# Attendre quelques secondes que l'app démarre
sleep 5

# Définir le webhook Telegram
python app/telegram/set_webhook.py

# Garder le processus actif
tail -f /dev/null
