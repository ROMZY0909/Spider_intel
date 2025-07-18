# app/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# ✅ Charge les variables d’environnement
load_dotenv()

# ✅ Instanciation de l’application
app = FastAPI(
    title=os.getenv("APP_NAME", "SPIDER_INTEL"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="🕷️ Plateforme de veille OSINT avec intégration Telegram, PDF, Supabase et APIs de sécurité."
)

# ✅ Middleware CORS (à restreindre en prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Inclusion des routes
try:
    from app.routes.email_route import router as EmailRouter
    from app.routes.auth_route import router as AuthRouter
    from app.telegram.webhook import router as TelegramWebhookRouter
except ModuleNotFoundError as e:
    # 🔥 Render échoue si le PYTHONPATH n'est pas correctement configuré
    # Ajout dynamique du chemin parent si nécessaire
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from app.routes.email_route import router as EmailRouter
    from app.routes.auth_route import router as AuthRouter
    from app.telegram.webhook import router as TelegramWebhookRouter

# ✅ Enregistrement des routes
app.include_router(EmailRouter, prefix="/email", tags=["Email OSINT"])
app.include_router(AuthRouter, prefix="/auth", tags=["Authentification"])
app.include_router(TelegramWebhookRouter, prefix="", tags=["Telegram Webhook"])

# ✅ Route de test
@app.get("/")
def read_root():
    return {
        "message": "✅ Bienvenue sur SPIDER INTEL !",
        "version": os.getenv("APP_VERSION", "1.0.0")
    }
