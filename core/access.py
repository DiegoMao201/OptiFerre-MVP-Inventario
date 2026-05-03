"""RBAC + paywall middleware para Streamlit.

Diseño:
- effective_plan(tenant_id): devuelve el plan considerado activo, mapeando
  trial vigente como acceso a Pro y trial vencido como sin acceso pago.
- require_feature(feature_key): devuelve True si la página puede continuar.
  Si no, renderiza el paywall correspondiente y devuelve False, de modo que
  la página haga `if not require_feature(...): return`.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

import streamlit as st
from sqlalchemy import select

from core.database import session_scope
from core.models import Subscription
from core.plans import (
    FEATURE_REQUIREMENTS,
    feature_enabled,
    has_minimum_plan,
    normalize_plan,
    plan_info,
    plan_rank,
)


def _subscription_row(tenant_id: int) -> Optional[Subscription]:
    with session_scope() as db:
        sub = db.scalar(select(Subscription).where(Subscription.tenant_id == tenant_id))
        if sub is None:
            return None
        # Desligar para que se pueda leer fuera de la sesión
        db.expunge(sub)
        return sub


def effective_plan(tenant_id: int) -> str:
    """Devuelve el plan operativo (no el literal del registro).

    Reglas:
    - active + plan en catálogo => ese plan
    - trialing y trial vigente => "pro" (queremos que sienta el valor)
    - trialing pero vencido => "starter" para no romper acceso básico
    - sin suscripción => "free"
    """
    sub = _subscription_row(tenant_id)
    if sub is None:
        return "free"
    if sub.status == "active" and sub.plan in {"starter", "pro", "enterprise"}:
        return sub.plan
    if sub.status == "trialing":
        if sub.trial_ends_at and sub.trial_ends_at >= datetime.utcnow():
            return "pro"
        return "starter"
    if sub.status in {"past_due", "canceled"}:
        return "free"
    return normalize_plan(sub.plan)


def require_feature(
    feature_key: str,
    *,
    user: dict,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> bool:
    """Si el feature está habilitado para el plan del tenant, devuelve True.
    Si no, renderiza un paywall elegante y devuelve False."""
    plan = effective_plan(user["tenant_id"])
    if feature_enabled(plan, feature_key):
        return True
    required_plan = FEATURE_REQUIREMENTS.get(feature_key, "pro")
    from ui.components import paywall_card  # import diferido para evitar ciclos
    paywall_card(
        current_plan=plan,
        required_plan=required_plan,
        feature_key=feature_key,
        title=title,
        description=description,
    )
    return False


def can(user: dict, feature_key: str) -> bool:
    """Versión silenciosa para checks dentro de un render."""
    return feature_enabled(effective_plan(user["tenant_id"]), feature_key)


def plan_summary(tenant_id: int) -> dict:
    plan = effective_plan(tenant_id)
    info = plan_info(plan) or {}
    return {
        "plan": plan,
        "rank": plan_rank(plan),
        "name": info.get("name", plan.capitalize()),
        "tagline": info.get("tagline", ""),
        "ai_persona": info.get("ai_persona", "concierge"),
    }


__all__ = [
    "effective_plan",
    "require_feature",
    "can",
    "plan_summary",
    "has_minimum_plan",
]
