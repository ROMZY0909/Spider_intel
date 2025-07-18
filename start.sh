#!/bin/bash
# Lancer FastAPI via Uvicorn (au premier plan)
echo "🚀 Démarrage de l'API avec Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
