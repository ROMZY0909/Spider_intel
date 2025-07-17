from pydantic import BaseModel, Field

class UserLogin(BaseModel):
    """Modèle pour la soumission des identifiants utilisateur"""
    username: str
    password: str

class UserToken(BaseModel):
    """Modèle retourné après authentification, contenant le JWT"""
    access_token: str
    token_type: str = Field(default="bearer", const=True)

class TokenPayload(BaseModel):
    """Données extraites du JWT (payload)"""
    sub: str  # Identifiant de l'utilisateur
    role: str  # Rôle de l'utilisateur (admin, analyste, etc.)
