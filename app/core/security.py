import os
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

# Clés de sécurité
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 120))

# Authentification via OAuth2 (Bearer token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_token(user_id: str, role: str, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    """Crée un token JWT encodé avec l’ID et le rôle de l’utilisateur"""
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + expires_delta
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Décode un token JWT, lève une erreur s’il est invalide ou expiré"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="⏳ Token expiré.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="❌ Token invalide.")


def get_current_user_role(token: str = Depends(oauth2_scheme)) -> str:
    """Retourne le rôle de l’utilisateur à partir du token"""
    payload = decode_token(token)
    return payload.get("role", "visiteur")


def require_role(roles: list[str]):
    """
    Vérifie que le rôle extrait du token est dans la liste autorisée.
    À utiliser avec Depends dans les routes protégées.
    """
    def role_dependency(current_role: str = Depends(get_current_user_role)):
        if current_role not in roles:
            raise HTTPException(status_code=403, detail="🔐 Accès interdit.")
    return role_dependency
