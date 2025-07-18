from pydantic import BaseModel
from typing import Optional, Literal


class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = False


class UserInDB(User):
    hashed_password: str


class UserToken(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"