"""Servicio de Órdenes de Compra: snapshot a OC + exportación Excel."""
from __future__ import annotations

import io
from datetime import datetime
from typing import Optional

import pandas as pd
from sqlalchemy import select

from core.database import session_scope, tenant_select
from core.models import (
    AuditLog,
    PurchaseOrder,
    PurchaseOrderItem,
    PurchaseSuggestion,
)


def _next_code(tenant_id: int, db) -> str:
    base = datetime.utcnow().strftime("OC-%Y%m%d")
    count = (
        db.scalar(
            select(PurchaseOrder).where(
                PurchaseOrder.tenant_id == tenant_id,
                PurchaseOrder.code.like(f"{base}%"),
            )
        )
        is not None
    )
    n = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.tenant_id == tenant_id,
            PurchaseOrder.code.like(f"{base}%"),
        )
        .count()
        if hasattr(db, "query")
        else 0
    )
    suffix = n + 1 if count else 1
    return f"{base}-{suffix:03d}"


def create_purchase_order_from_suggestions(
    tenant_id: int,
    *,
    only_skus: Optional[list[str]] = None,
    notes: Optional[str] = None,
    created_by: Optional[str] = None,
) -> dict:
    """Crea una OC con los items marcados como included en purchase_suggestions."""
    with session_scope(tenant_id=tenant_id) as db:
        stmt = tenant_select(db, PurchaseSuggestion).where(
            PurchaseSuggestion.included.is_(True)
        )
        if only_skus:
            stmt = stmt.where(PurchaseSuggestion.sku.in_(only_skus))
        rows = db.scalars(stmt).all()
        rows = [r for r in rows if r.effective_qty > 0]
        if not rows:
            return {"ok": False, "reason": "no_items"}

        code = _next_code(tenant_id, db)
        order = PurchaseOrder(
            tenant_id=tenant_id,
            code=code,
            status="draft",
            notes=notes,
            created_by=created_by,
        )
        db.add(order)
        db.flush()

        total_units = 0.0
        total_amount = 0.0
        for r in rows:
            qty = r.effective_qty
            line_total = qty * float(r.unit_cost or 0)
            db.add(
                PurchaseOrderItem(
                    order_id=order.id,
                    sku=r.sku,
                    name=r.name,
                    qty=qty,
                    unit_cost=float(r.unit_cost or 0),
                    line_total=line_total,
                )
            )
            total_units += qty
            total_amount += line_total
        order.total_units = total_units
        order.total_amount = total_amount

        db.add(
            AuditLog(
                tenant_id=tenant_id,
                user_email=created_by,
                action="purchase_order_created",
                entity="purchase_order",
                notes=f"code={code} items={len(rows)} total={total_amount:.2f}",
            )
        )
        return {
            "ok": True,
            "id": order.id,
            "code": code,
            "items": len(rows),
            "total_units": total_units,
            "total_amount": total_amount,
        }


def list_orders(tenant_id: int, limit: int = 25) -> list[dict]:
    with session_scope(tenant_id=tenant_id) as db:
        rows = (
            db.scalars(
                tenant_select(db, PurchaseOrder).order_by(PurchaseOrder.id.desc()).limit(limit)
            ).all()
        )
        return [
            {
                "id": r.id,
                "code": r.code,
                "status": r.status,
                "total_units": float(r.total_units),
                "total_amount": float(r.total_amount),
                "created_at": r.created_at,
                "created_by": r.created_by,
            }
            for r in rows
        ]


def export_order_excel(tenant_id: int, order_id: int) -> Optional[bytes]:
    with session_scope(tenant_id=tenant_id) as db:
        order = db.scalar(
            tenant_select(db, PurchaseOrder).where(PurchaseOrder.id == order_id)
        )
        if order is None:
            return None
        items = list(order.items)
        df = pd.DataFrame(
            [
                {
                    "SKU": it.sku,
                    "Nombre": it.name,
                    "Cantidad": it.qty,
                    "Costo unitario": it.unit_cost,
                    "Total línea": it.line_total,
                }
                for it in items
            ]
        )
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Orden de Compra")
            meta = pd.DataFrame(
                [
                    {"Campo": "Código", "Valor": order.code},
                    {"Campo": "Estado", "Valor": order.status},
                    {"Campo": "Total unidades", "Valor": order.total_units},
                    {"Campo": "Total monto", "Valor": order.total_amount},
                    {"Campo": "Creado por", "Valor": order.created_by or ""},
                    {"Campo": "Creado el", "Valor": order.created_at.isoformat() if order.created_at else ""},
                ]
            )
            meta.to_excel(writer, index=False, sheet_name="Cabecera")
        return buffer.getvalue()


__all__ = [
    "create_purchase_order_from_suggestions",
    "list_orders",
    "export_order_excel",
]
