# app/service/auth_service.py

from app.models.user_model import User  # facultatif si tu as un modèle
from passlib.context import CryptContext

# Initialisation du contexte de hachage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fonction simulée d'authentification d'utilisateur
def authenticate_user(email: str, password: str):
    # Pour le moment, retourne toujours False pour désactiver l'authentification réelle
    # Tu peux remplacer ceci par une logique Supabase plus tard
    return False

# Fonction utilitaire pour vérifier un mot de passe haché (optionnel si utile dans d'autres modules)
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
