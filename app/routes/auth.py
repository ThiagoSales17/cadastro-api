import secrets

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.auth import create_token
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/token", response_model=TokenResponse)
async def login(data: LoginRequest):
    if not secrets.compare_digest(data.username, settings.auth_username) or not secrets.compare_digest(
        data.password, settings.auth_password
    ):
        raise HTTPException(401, "Invalid credentials")
    return TokenResponse(access_token=create_token(data.username))
