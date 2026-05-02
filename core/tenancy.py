"""Capa de multi-tenancy: lectura/actualización de marca y configuración por tenant."""
from __future__ import annotations

from typing import Optional

from sqlalchemy import select

from core.database import session_scope
from core.models import Tenant


def get_tenant(tenant_id: int) -> Optional[dict]:
    with session_scope() as db:
        t = db.get(Tenant, tenant_id)
        if not t:
            return None
        return {
            "id": t.id,
            "slug": t.slug,
            "company_name": t.company_name,
            "brand_primary_color": t.brand_primary_color,
            "brand_logo_url": t.brand_logo_url,
            "theme_mode": t.theme_mode,
        }


def update_brand(
    tenant_id: int,
    company_name: Optional[str] = None,
    primary_color: Optional[str] = None,
    logo_url: Optional[str] = None,
    theme_mode: Optional[str] = None,
) -> None:
    with session_scope() as db:
        t = db.get(Tenant, tenant_id)
        if not t:
            return
        if company_name:
            t.company_name = company_name
        if primary_color:
            t.brand_primary_color = primary_color
        if logo_url is not None:
            t.brand_logo_url = logo_url or None
        if theme_mode in {"dark", "light"}:
            t.theme_mode = theme_mode


def list_tenants() -> list[dict]:
    with session_scope() as db:
        rows = db.scalars(select(Tenant).order_by(Tenant.created_at.desc())).all()
        return [
            {
                "id": r.id,
                "slug": r.slug,
                "company_name": r.company_name,
                "created_at": r.created_at,
            }
            for r in rows
        ]
