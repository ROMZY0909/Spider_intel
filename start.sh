#!/bin/bash

# Définir le webhook en tâche de fond (facultatif mais propre)
python app/telegram/set_webhook.py &

# Démarrer FastAPI au premier plan (Render surveille ce process)
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
