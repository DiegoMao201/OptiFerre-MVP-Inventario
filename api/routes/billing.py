"""Endpoints de planes y suscripción."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.deps.security import get_current_user
from core.billing import create_checkout_session, get_subscription
from core.config import get_settings
from core.plans import public_catalog

router = APIRouter()


class CheckoutRequest(BaseModel):
    plan: str


@router.get("/plans")
def plans() -> dict:
    settings = get_settings()
    items = []
    for key, plan in public_catalog():
        items.append(
            {
                "key": key,
                "name": plan["name"],
                "tagline": plan["tagline"],
                "summary": plan["summary"],
                "sales_pitch": plan["sales_pitch"],
                "upgrade_trigger": plan["upgrade_trigger"],
                "cta_label": plan["cta_label"],
                "price_monthly_usd": plan["price_monthly_usd"],
                "features": plan["features"],
                "ai_capabilities": plan["ai_capabilities"],
                "sales_email": settings.sales_email,
                "sales_phone": settings.sales_phone,
            }
        )
    return {"plans": items}


@router.get("/subscription")
def subscription(current_user: dict = Depends(get_current_user)) -> dict:
    current = get_subscription(current_user["tenant_id"])
    return {
        "subscription": current,
        "sales_email": get_settings().sales_email,
        "sales_phone": get_settings().sales_phone,
    }


@router.post("/checkout")
def checkout(payload: CheckoutRequest, current_user: dict = Depends(get_current_user)) -> dict:
    try:
        return create_checkout_session(current_user["tenant_id"], current_user["email"], payload.plan)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc