# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Chargement des variables d’environnement
load_dotenv()

# Importation des routes
from app.routes.email_route import router as EmailRouter
from app.routes.auth_route import router as AuthRouter

# Création de l'application FastAPI
app = FastAPI(
    title=os.getenv("APP_NAME", "SPIDER_INTEL"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="🕷️ Plateforme de veille OSINT avec intégration Telegram, PDF, Supabase et APIs de sécurité."
)

# Configuration des CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(EmailRouter, prefix="/email", tags=["Email OSINT"])
app.include_router(AuthRouter, prefix="/auth", tags=["Authentification"])

# Route de test
@app.get("/")
def read_root():
    return {
        "message": "✅ Bienvenue sur SPIDER INTEL !",
        "version": os.getenv("APP_VERSION", "1.0.0")
    }
