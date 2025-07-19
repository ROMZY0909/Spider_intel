# app/main.py

import os
import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import ipaddress

# ✅ Chargement des variables d’environnement
load_dotenv()

# ✅ Création de l'application FastAPI
app = FastAPI(
    title=os.getenv("APP_NAME", "SPIDER_INTEL"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="🕷️ Plateforme de veille OSINT avec intégration Telegram, PDF, Supabase et APIs de sécurité."
)

# ✅ Middleware CORS (à restreindre en production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Détermination du chemin absolu vers templates (compatible Render & local)
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ✅ Inclusion dynamique des routes (Render + local compatible)
try:
    from app.routes.email_route import router as EmailRouter
    from app.routes.auth_route import router as AuthRouter
    from app.telegram.webhook import router as TelegramWebhookRouter
except ModuleNotFoundError:
    sys.path.append(str(BASE_DIR.parent))
    from app.routes.email_route import router as EmailRouter
    from app.routes.auth_route import router as AuthRouter
    from app.telegram.webhook import router as TelegramWebhookRouter

# ✅ Enregistrement des routes
app.include_router(EmailRouter, prefix="/email", tags=["Email OSINT"])
app.include_router(AuthRouter, prefix="/auth", tags=["Authentification"])
app.include_router(TelegramWebhookRouter, prefix="", tags=["Telegram Webhook"])

# ✅ Import de la fonction de scan depuis email_scanner.py
from app.scanner.email_scanner import full_osint_lookup

# ✅ Route d'accueil : interface web
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Endpoint pour simuler un scan via l’interface web
@app.post("/simulate_bot")
async def simulate_bot(request: Request):
    data = await request.json()
    command = data.get("command")

    if not command or not command.startswith("/scan "):
        return JSONResponse({"message": "❌ Commande invalide."}, status_code=400)

    ip = command.split("/scan ")[1].strip()

    try:
        ipaddress.ip_address(ip)  # Validation IP
    except ValueError:
        return JSONResponse({"message": "❌ Adresse IP invalide."}, status_code=400)

    try:
        result = full_osint_lookup(ip)
        return JSONResponse({"message": result})
    except Exception as e:
        return JSONResponse({"message": f"❌ Erreur lors du scan : {str(e)}"}, status_code=500)
