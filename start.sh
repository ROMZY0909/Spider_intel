#!/bin/bash
# Démarrer FastAPI via Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000} &

# Attendre que le serveur démarre
sleep 5

# Définir le webhook
python app/telegram/set_webhook.py

# Garder le container actif
tail -f /dev/null
