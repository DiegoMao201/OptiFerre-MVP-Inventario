"""Endpoints de autenticación."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from api.deps.security import create_access_token, get_current_user
from api.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from core.auth import authenticate, register_tenant
from core.mail import send_account_created_email, send_login_notice_email

router = APIRouter()


def _to_token_response(session_data: dict) -> TokenResponse:
    token = create_access_token(
        user_id=session_data["user_id"],
        tenant_id=session_data["tenant_id"],
        email=session_data["email"],
        role=session_data["role"],
    )
    return TokenResponse(access_token=token, user=UserResponse(**session_data))


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest) -> TokenResponse:
    try:
        register_tenant(
            payload.company_name,
            payload.email,
            payload.password,
            payload.full_name,
        )
    except Exception as exc:  # pragma: no cover - integridad/duplicados
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"No fue posible crear la cuenta: {exc}") from exc

    session_data = authenticate(payload.email, payload.password)
    if not session_data:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Cuenta creada pero no fue posible autenticar.")

    try:
        send_account_created_email(
            session_data["email"], session_data["full_name"], session_data["company_name"]
        )
    except Exception:
        pass

    return _to_token_response(session_data)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    session_data = authenticate(payload.email, payload.password)
    if not session_data:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Correo o contraseña incorrectos.")

    try:
        send_login_notice_email(
            session_data["email"], session_data["full_name"], session_data["company_name"]
        )
    except Exception:
        pass

    return _to_token_response(session_data)


@router.get("/me", response_model=UserResponse)
def me(current_user: dict = Depends(get_current_user)) -> UserResponse:
    return UserResponse(**current_user)
