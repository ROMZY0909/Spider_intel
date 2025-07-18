#!/bin/bash

# Activer le PYTHONPATH (utile pour Render)
export PYTHONPATH=$(pwd)

# Démarrer FastAPI via Uvicorn (ne pas mettre en arrière-plan)
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
