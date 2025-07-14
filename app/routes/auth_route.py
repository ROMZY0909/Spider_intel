from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_token
from app.models.user_model import UserToken

router = APIRouter()

# ⚠️ Simuler un user "en dur" (à remplacer plus tard par DB)
fake_users_db = {
    "admin": {"password": "admin123", "role": "admin"},
    "analyste": {"password": "osint2025", "role": "analyste"},
    "invite": {"password": "invite", "role": "visiteur"}
}

@router.post("/auth/token", response_model=UserToken)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token = create_token(user_id=form_data.username, role=user["role"])
    return UserToken(access_token=token)
