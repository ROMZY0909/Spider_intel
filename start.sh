#!/bin/bash

# Start FastAPI with Uvicorn
echo "🚀 Starting Uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000} || {
    echo "❌ Uvicorn failed to start."
    exit 1
}

# Set Telegram Webhook
echo "📡 Setting Telegram webhook..."
python app/telegram/set_webhook.py || {
    echo "❌ Failed to set webhook."
    exit 1
}

# Keep container alive
tail -f /dev/null
