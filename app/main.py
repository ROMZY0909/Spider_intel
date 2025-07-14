from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Création de l'application FastAPI
app = FastAPI(
    title="SPIDER INTEL 🕷️",
    description="Plateforme OSINT automatisée — Surveillance, analyse, alerte.",
    version="1.0.0"
)

# Middleware CORS (à restreindre en production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En prod : ["https://ton-front.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importer et inclure les routes
from app.routes import email_route

app.include_router(email_route.router, prefix="/scan", tags=["Scan Email"])

# Route racine
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur SPIDER INTEL API 🕷️"}
