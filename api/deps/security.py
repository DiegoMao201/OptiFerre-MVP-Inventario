"""JWT y dependencias de seguridad para la API."""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from core.config import get_settings
from core.database import session_scope
from core.models import Tenant, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

JWT_ALG = "HS256"
JWT_EXPIRES_MINUTES = int(os.getenv("API_JWT_EXPIRES_MINUTES", "1440"))


def _secret() -> str:
    return get_settings().secret_key or "dev-secret-change-me"


def create_access_token(
    *,
    user_id: int,
    tenant_id: int,
    email: str,
    role: str,
    expires_minutes: Optional[int] = None,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or JWT_EXPIRES_MINUTES)
    payload = {
        "sub": str(user_id),
        "tid": tenant_id,
        "email": email,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, _secret(), algorithm=JWT_ALG)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, _secret(), algorithms=[JWT_ALG])
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expirado") from exc
    except jwt.PyJWTError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token inválido") from exc


def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> dict:
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Falta token de acceso")
    payload = decode_token(token)
    user_id = int(payload.get("sub", 0))
    with session_scope() as db:
        user = db.scalar(select(User).where(User.id == user_id, User.is_active.is_(True)))
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuario no encontrado")
        tenant = db.get(Tenant, user.tenant_id)
        return {
            "user_id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "tenant_id": tenant.id,
            "tenant_slug": tenant.slug,
            "company_name": tenant.company_name,
        }
