"""Endpoints de autenticación."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from api.deps.security import create_access_token, get_current_user
from api.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserResponse,
)
from core.auth import (
    authenticate,
    create_password_reset_request,
    register_tenant,
    reset_password_with_token,
    validate_password_reset_token,
)
from core.config import get_settings
from core.mail import (
    send_account_created_email,
    send_login_notice_email,
    send_password_changed_email,
    send_password_reset_email,
)

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
    except IntegrityError as exc:  # pragma: no cover - integridad/duplicados
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Ya existe una cuenta registrada con ese correo.",
        ) from exc
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


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(payload: ForgotPasswordRequest) -> MessageResponse:
    reset_request = create_password_reset_request(payload.email)
    if reset_request:
        reset_url = f"{get_settings().base_url.rstrip('/')}/reset-password?token={reset_request['token']}"
        try:
            send_password_reset_email(
                reset_request["email"],
                reset_request["full_name"],
                reset_url,
            )
        except Exception:
            pass

    return MessageResponse(
        message="Si encontramos una cuenta con ese correo, te enviamos un enlace para recuperar el acceso."
    )


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(payload: ResetPasswordRequest) -> MessageResponse:
    if not validate_password_reset_token(payload.token):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "El enlace de recuperación es inválido o ya venció.",
        )

    result = reset_password_with_token(payload.token, payload.password)
    if not result:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "No fue posible actualizar la contraseña con ese enlace.",
        )

    try:
        send_password_changed_email(result["email"], result["full_name"])
    except Exception:
        pass

    return MessageResponse(message="Tu contraseña fue actualizada. Ya puedes entrar con la nueva clave.")


@router.get("/me", response_model=UserResponse)
def me(current_user: dict = Depends(get_current_user)) -> UserResponse:
    return UserResponse(**current_user)
