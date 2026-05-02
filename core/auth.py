"""Autenticación: hashing bcrypt + helpers de sesión Streamlit."""
from __future__ import annotations

import re
import secrets
from datetime import datetime, timedelta
from typing import Optional

import streamlit as st
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select

from core.database import session_scope
from core.models import PasswordResetToken, Subscription, Tenant, User

_SLUG_RE = re.compile(r"[^a-z0-9]+")
_PASSWORD_RESET_HOURS = 2


def _slugify(value: str) -> str:
    return _SLUG_RE.sub("-", value.lower()).strip("-") or "tenant"


def hash_password(plain: str) -> str:
    return pbkdf2_sha256.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return pbkdf2_sha256.verify(plain, hashed)
    except Exception:
        return False


def register_tenant(company_name: str, email: str, password: str, full_name: str) -> User:
    """Crea Tenant + User owner + Subscription trial (14 días)."""
    slug_base = _slugify(company_name)
    with session_scope() as db:
        # asegura slug único
        slug = slug_base
        idx = 1
        while db.scalar(select(Tenant).where(Tenant.slug == slug)):
            idx += 1
            slug = f"{slug_base}-{idx}"

        tenant = Tenant(slug=slug, company_name=company_name)
        db.add(tenant)
        db.flush()

        user = User(
            tenant_id=tenant.id,
            email=email.lower().strip(),
            password_hash=hash_password(password),
            full_name=full_name,
            role="owner",
        )
        sub = Subscription(
            tenant_id=tenant.id,
            plan="trial",
            status="trialing",
            trial_ends_at=datetime.utcnow() + timedelta(days=14),
        )
        db.add_all([user, sub])
        db.flush()
        db.refresh(user)
        # Desligar de la sesión para devolver a UI
        db.expunge(user)
        return user


def authenticate(email: str, password: str) -> Optional[dict]:
    """Devuelve dict con datos de sesión si las credenciales son válidas."""
    with session_scope() as db:
        user = db.scalar(select(User).where(User.email == email.lower().strip()))
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.password_hash):
            return None
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


def create_password_reset_request(email: str) -> Optional[dict]:
    normalized = email.lower().strip()
    with session_scope() as db:
        user = db.scalar(select(User).where(User.email == normalized, User.is_active.is_(True)))
        if not user:
            return None

        active_tokens = db.scalars(
            select(PasswordResetToken).where(
                PasswordResetToken.user_id == user.id,
                PasswordResetToken.used_at.is_(None),
            )
        ).all()
        now = datetime.utcnow()
        for token_row in active_tokens:
            token_row.used_at = now

        token = secrets.token_urlsafe(32)
        row = PasswordResetToken(
            user_id=user.id,
            token=token,
            expires_at=now + timedelta(hours=_PASSWORD_RESET_HOURS),
        )
        db.add(row)
        tenant = db.get(Tenant, user.tenant_id)
        return {
            "token": token,
            "email": user.email,
            "full_name": user.full_name,
            "company_name": tenant.company_name if tenant else "tu empresa",
            "expires_at": row.expires_at,
        }


def validate_password_reset_token(token: str) -> Optional[dict]:
    with session_scope() as db:
        row = db.scalar(select(PasswordResetToken).where(PasswordResetToken.token == token.strip()))
        if not row or row.used_at is not None or row.expires_at < datetime.utcnow():
            return None
        user = db.get(User, row.user_id)
        if not user or not user.is_active:
            return None
        tenant = db.get(Tenant, user.tenant_id)
        return {
            "email": user.email,
            "full_name": user.full_name,
            "company_name": tenant.company_name if tenant else "tu empresa",
            "expires_at": row.expires_at,
        }


def reset_password_with_token(token: str, new_password: str) -> Optional[dict]:
    with session_scope() as db:
        row = db.scalar(select(PasswordResetToken).where(PasswordResetToken.token == token.strip()))
        if not row or row.used_at is not None or row.expires_at < datetime.utcnow():
            return None

        user = db.get(User, row.user_id)
        if not user or not user.is_active:
            return None

        user.password_hash = hash_password(new_password)
        row.used_at = datetime.utcnow()
        tenant = db.get(Tenant, user.tenant_id)
        return {
            "email": user.email,
            "full_name": user.full_name,
            "company_name": tenant.company_name if tenant else "tu empresa",
        }


def login(session_data: dict) -> None:
    st.session_state["auth"] = session_data


def logout() -> None:
    for key in (
        "auth",
        "uploaded_inventory",
        "uploaded_sales",
        "analysis_result",
        "demo_mode",
        "cfg_service_level",
        "cfg_horizon_days",
        "_last_persisted_analysis_signature",
    ):
        st.session_state.pop(key, None)


def current_user() -> Optional[dict]:
    return st.session_state.get("auth")


def require_login() -> dict:
    user = current_user()
    if not user:
        st.warning("🔒 Debes iniciar sesión para acceder.")
        st.stop()
    return user
