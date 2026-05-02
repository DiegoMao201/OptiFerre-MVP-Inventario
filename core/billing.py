"""Integración Stripe para suscripciones SaaS.

Diseñado para degradar de forma elegante: si Stripe no está configurado, las
funciones devuelven datos de simulación para no romper el flujo del MVP.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select

from core.config import get_settings
from core.database import session_scope, tenant_select, tenant_session_scope
from core.models import Subscription, Tenant

try:
    import stripe  # type: ignore
except Exception:  # pragma: no cover
    stripe = None  # type: ignore


PLAN_CATALOG = {
    "starter": {
        "name": "Starter",
        "price_monthly_usd": 49,
        "features": [
            "Hasta 2.000 SKUs",
            "Análisis ABC/XYZ",
            "Stock de seguridad y ROP",
            "Soporte por email",
        ],
    },
    "pro": {
        "name": "Pro",
        "price_monthly_usd": 149,
        "features": [
            "Hasta 25.000 SKUs",
            "Multi-bodega",
            "Reglas de compra avanzadas",
            "Soporte prioritario",
        ],
    },
    "enterprise": {
        "name": "Enterprise",
        "price_monthly_usd": 499,
        "features": [
            "SKUs ilimitados",
            "Usuarios ilimitados",
            "White-label completo",
            "Onboarding dedicado",
        ],
    },
}


def _configure_stripe() -> bool:
    settings = get_settings()
    if not settings.stripe_enabled or stripe is None:
        return False
    stripe.api_key = settings.stripe_secret_key
    return True


def _price_id_for(plan: str) -> Optional[str]:
    s = get_settings()
    return {
        "starter": s.stripe_price_starter,
        "pro": s.stripe_price_pro,
        "enterprise": s.stripe_price_enterprise,
    }.get(plan)


def get_subscription(tenant_id: int) -> Optional[dict]:
    with tenant_session_scope(tenant_id=tenant_id) as db:
        sub = db.scalar(tenant_select(db, Subscription))
        if not sub:
            return None
        return {
            "plan": sub.plan,
            "status": sub.status,
            "is_active": sub.is_active(),
            "current_period_end": sub.current_period_end,
            "trial_ends_at": sub.trial_ends_at,
            "stripe_customer_id": sub.stripe_customer_id,
            "stripe_subscription_id": sub.stripe_subscription_id,
        }


def has_active_access(tenant_id: int) -> bool:
    sub = get_subscription(tenant_id)
    return bool(sub and sub["is_active"])


def create_checkout_session(
    tenant_id: int, customer_email: str, plan: str
) -> dict:
    """Crea una Stripe Checkout Session. Devuelve {url, mode}."""
    settings = get_settings()
    if plan not in PLAN_CATALOG:
        raise ValueError(f"Plan inválido: {plan}")

    if not _configure_stripe():
        # Modo simulación: activa la suscripción localmente para demo.
        _simulate_activation(tenant_id, plan)
        return {
            "url": None,
            "mode": "simulated",
            "message": (
                "Stripe no está configurado. Se activó una suscripción de demostración "
                f"con el plan {PLAN_CATALOG[plan]['name']}."
            ),
        }

    price_id = _price_id_for(plan)
    if not price_id:
        raise RuntimeError(f"Falta STRIPE_PRICE_* para el plan {plan}")

    session = stripe.checkout.Session.create(
        mode="subscription",
        customer_email=customer_email,
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=f"{settings.base_url}/?checkout=success&plan={plan}",
        cancel_url=f"{settings.base_url}/?checkout=cancel",
        metadata={"tenant_id": str(tenant_id), "plan": plan},
        subscription_data={"metadata": {"tenant_id": str(tenant_id), "plan": plan}},
        allow_promotion_codes=True,
    )
    return {"url": session.url, "mode": "stripe", "id": session.id}


def _simulate_activation(tenant_id: int, plan: str) -> None:
    with tenant_session_scope(tenant_id=tenant_id) as db:
        sub = db.scalar(tenant_select(db, Subscription))
        if not sub:
            sub = Subscription(tenant_id=tenant_id)
            db.add(sub)
        sub.plan = plan
        sub.status = "active"
        sub.current_period_end = datetime.utcnow() + timedelta(days=30)


def handle_webhook_event(payload: bytes, sig_header: str) -> dict:
    """Procesa un webhook de Stripe (uso futuro vía endpoint externo)."""
    settings = get_settings()
    if not _configure_stripe() or not settings.stripe_webhook_secret:
        return {"ok": False, "reason": "stripe_not_configured"}

    event = stripe.Webhook.construct_event(payload, sig_header, settings.stripe_webhook_secret)
    etype = event["type"]
    obj = event["data"]["object"]
    tenant_id = int((obj.get("metadata") or {}).get("tenant_id", 0)) or None

    if not tenant_id:
        return {"ok": True, "ignored": True}

    with tenant_session_scope(tenant_id=tenant_id) as db:
        sub = db.scalar(tenant_select(db, Subscription))
        if not sub:
            sub = Subscription(tenant_id=tenant_id)
            db.add(sub)

        if etype in {"checkout.session.completed", "customer.subscription.created",
                     "customer.subscription.updated"}:
            sub.status = obj.get("status", "active")
            sub.stripe_customer_id = obj.get("customer") or sub.stripe_customer_id
            sub.stripe_subscription_id = obj.get("subscription") or obj.get("id")
            plan = (obj.get("metadata") or {}).get("plan")
            if plan in PLAN_CATALOG:
                sub.plan = plan
            cpe = obj.get("current_period_end")
            if cpe:
                sub.current_period_end = datetime.utcfromtimestamp(cpe)
        elif etype == "customer.subscription.deleted":
            sub.status = "canceled"

    return {"ok": True, "type": etype}
