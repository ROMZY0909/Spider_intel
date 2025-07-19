# app/main.py

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# ✅ Chargement des variables d’environnement
load_dotenv()

# ✅ Création de l'application FastAPI
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

# ✅ Configuration des templates HTML
templates = Jinja2Templates(directory="app/templates")

# ✅ Inclusion des routes Telegram / Email / Auth
try:
    from app.routes.email_route import router as EmailRouter
    from app.routes.auth_route import router as AuthRouter
    from app.telegram.webhook import router as TelegramWebhookRouter
except ModuleNotFoundError as e:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from app.routes.email_route import router as EmailRouter
    from app.routes.auth_route import router as AuthRouter
    from app.telegram.webhook import router as TelegramWebhookRouter

app.include_router(EmailRouter, prefix="/email", tags=["Email OSINT"])
app.include_router(AuthRouter, prefix="/auth", tags=["Authentification"])
app.include_router(TelegramWebhookRouter, prefix="", tags=["Telegram Webhook"])

# ✅ Route HTML principale (index)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
