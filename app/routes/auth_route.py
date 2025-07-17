# app/routes/auth_route.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import authenticate_user
from app.models.user_model import UserToken

router = APIRouter()

@router.post("/token", response_model=UserToken)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authentifie un utilisateur avec username/password et retourne un JWT.
    """
    token = authenticate_user(form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    return UserToken(access_token=token)
