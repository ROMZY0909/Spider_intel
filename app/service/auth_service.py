# app/services/auth_service.py

import os
import bcrypt
from dotenv import load_dotenv
from app.core.security import create_token

load_dotenv()

# Connexion unique à la base de données Supabase
conn = psycopg2.connect(
    host=os.getenv("SUPABASE_DB_HOST"),
    port=os.getenv("SUPABASE_DB_PORT", 5432),
    database=os.getenv("SUPABASE_DB_NAME"),
    user=os.getenv("SUPABASE_DB_USER"),
    password=os.getenv("SUPABASE_DB_PASSWORD")
)


def get_user_by_username(username: str):
    """
    Recherche un utilisateur dans la table 'users' par son nom d'utilisateur.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT username, password_hash, role FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        if result:
            return {
                "username": result[0],
                "password_hash": result[1],
                "role": result[2]
            }
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie qu’un mot de passe correspond au hash stocké dans la base.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def authenticate_user(username: str, password: str):
    """
    Authentifie l'utilisateur en vérifiant les identifiants et retourne un JWT.
    """
    user = get_user_by_username(username)
    if not user or not verify_password(password, user["password_hash"]):
        return None

    # Génère un JWT avec l'identité et le rôle de l'utilisateur
    return create_token(user_id=user["username"], role=user["role"])

