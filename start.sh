#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:/opt/render/project/src"

uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}

sleep 5
python app/telegram/set_webhook.py

tail -f /dev/null
