"""Persistencia de snapshots y UPSERT de sugerencias editables."""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional

import pandas as pd
from sqlalchemy import select

from core.database import session_scope, tenant_select
from core.models import (
    AIActionLog,
    InventorySnapshot,
    PurchaseSuggestion,
    SalesSnapshot,
)


def _val(row: dict, *keys, default=None):
    for k in keys:
        if k in row and row[k] not in (None, ""):
            return row[k]
    return default


def upsert_inventory_snapshot(tenant_id: int, df: pd.DataFrame) -> int:
    """Recibe un DF de inventario ya limpio y persiste un snapshot por SKU."""
    if df is None or df.empty:
        return 0
    count = 0
    with session_scope(tenant_id=tenant_id) as db:
        existing = {
            row.sku: row
            for row in db.scalars(tenant_select(db, InventorySnapshot)).all()
        }
        for _, raw in df.iterrows():
            r = raw.to_dict()
            sku = str(_val(r, "sku", default="")).strip()
            if not sku:
                continue
            entry = existing.get(sku)
            on_hand = float(_val(r, "stock_actual", "on_hand", default=0) or 0)
            avg_cost = float(_val(r, "costo_unitario", "avg_cost", default=0) or 0)
            name = _val(r, "nombre_comercial", "nombre", "name")
            category = _val(r, "categoria", "category")
            lead_time = _val(r, "lead_time_dias", "lead_time_days")
            pack = _val(r, "unidad_empaque_minimo", "pack_size")
            if entry is None:
                db.add(
                    InventorySnapshot(
                        tenant_id=tenant_id,
                        sku=sku,
                        name=name,
                        category=category,
                        on_hand=on_hand,
                        avg_cost=avg_cost,
                        lead_time_days=float(lead_time) if lead_time is not None else None,
                        pack_size=float(pack) if pack is not None else None,
                    )
                )
            else:
                entry.name = name or entry.name
                entry.category = category or entry.category
                entry.on_hand = on_hand
                entry.avg_cost = avg_cost
                if lead_time is not None:
                    entry.lead_time_days = float(lead_time)
                if pack is not None:
                    entry.pack_size = float(pack)
            count += 1
    return count


def upsert_sales_snapshot(
    tenant_id: int,
    df: pd.DataFrame,
    *,
    period_start: Optional[datetime] = None,
    period_end: Optional[datetime] = None,
) -> int:
    """Persiste un agregado por SKU dentro del período indicado."""
    if df is None or df.empty:
        return 0
    if period_start is None:
        period_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if period_end is None:
        period_end = datetime.utcnow()

    grouped = (
        df.assign(_units=df.get("cantidad", 0), _rev=df.get("valor_neto", df.get("valor", 0)))
        .groupby(df["sku"].astype(str).str.strip(), as_index=False)
        .agg(units_sold=("_units", "sum"), revenue=("_rev", "sum"))
    )
    count = 0
    with session_scope(tenant_id=tenant_id) as db:
        for _, row in grouped.iterrows():
            sku = str(row["sku"]).strip()
            if not sku:
                continue
            existing = db.scalar(
                select(SalesSnapshot).where(
                    SalesSnapshot.tenant_id == tenant_id,
                    SalesSnapshot.sku == sku,
                    SalesSnapshot.period_start == period_start,
                    SalesSnapshot.period_end == period_end,
                )
            )
            if existing is None:
                db.add(
                    SalesSnapshot(
                        tenant_id=tenant_id,
                        sku=sku,
                        period_start=period_start,
                        period_end=period_end,
                        units_sold=float(row["units_sold"] or 0),
                        revenue=float(row["revenue"] or 0),
                    )
                )
            else:
                existing.units_sold = float(row["units_sold"] or 0)
                existing.revenue = float(row["revenue"] or 0)
            count += 1
    return count


def upsert_suggestions_from_analysis(
    tenant_id: int,
    df: pd.DataFrame,
    *,
    run_id: Optional[int] = None,
    updated_by: Optional[str] = None,
) -> int:
    """Toma el DF resultante de full_analysis y persiste sugerencia por SKU.

    Respeta los ajustes manuales previos del usuario: no sobreescribe qty_user
    si ya existe."""
    if df is None or df.empty:
        return 0
    relevant = df[df.get("sugerencia_compra", 0) > 0]
    if relevant.empty:
        relevant = df  # mantén también las que están en 0 para visibilidad

    count = 0
    with session_scope(tenant_id=tenant_id) as db:
        existing = {
            row.sku: row
            for row in db.scalars(tenant_select(db, PurchaseSuggestion)).all()
        }
        for _, raw in relevant.iterrows():
            r = raw.to_dict()
            sku = str(_val(r, "sku", default="")).strip()
            if not sku:
                continue
            qty_ai = float(_val(r, "sugerencia_compra", default=0) or 0)
            unit_cost = float(_val(r, "costo_unitario", default=0) or 0)
            name = _val(r, "nombre_comercial", "nombre")
            entry = existing.get(sku)
            if entry is None:
                db.add(
                    PurchaseSuggestion(
                        tenant_id=tenant_id,
                        run_id=run_id,
                        sku=sku,
                        name=name,
                        qty_ai=qty_ai,
                        unit_cost=unit_cost,
                        included=qty_ai > 0,
                        updated_by=updated_by,
                    )
                )
            else:
                entry.qty_ai = qty_ai
                entry.unit_cost = unit_cost
                entry.name = name or entry.name
                entry.run_id = run_id
                # qty_user se respeta. included se preserva salvo que nunca se haya tocado.
            count += 1
    return count


def list_suggestions(tenant_id: int) -> list[dict]:
    with session_scope(tenant_id=tenant_id) as db:
        rows = db.scalars(tenant_select(db, PurchaseSuggestion)).all()
        return [
            {
                "id": r.id,
                "sku": r.sku,
                "name": r.name,
                "qty_ai": float(r.qty_ai),
                "qty_user": float(r.qty_user) if r.qty_user is not None else None,
                "unit_cost": float(r.unit_cost),
                "included": bool(r.included),
                "notes": r.notes,
                "updated_at": r.updated_at,
            }
            for r in rows
        ]


def apply_suggestion_edits(
    tenant_id: int, edits: Iterable[dict], updated_by: Optional[str] = None
) -> int:
    """Persiste cambios manuales hechos por el usuario sobre la tabla."""
    edits = list(edits)
    if not edits:
        return 0
    by_sku = {str(e["sku"]).strip(): e for e in edits if e.get("sku")}
    if not by_sku:
        return 0
    count = 0
    with session_scope(tenant_id=tenant_id) as db:
        rows = db.scalars(
            select(PurchaseSuggestion).where(
                PurchaseSuggestion.tenant_id == tenant_id,
                PurchaseSuggestion.sku.in_(list(by_sku.keys())),
            )
        ).all()
        index = {r.sku: r for r in rows}
        for sku, e in by_sku.items():
            row = index.get(sku)
            if row is None:
                row = PurchaseSuggestion(
                    tenant_id=tenant_id,
                    sku=sku,
                    name=e.get("name"),
                    qty_ai=float(e.get("qty_ai", 0) or 0),
                    unit_cost=float(e.get("unit_cost", 0) or 0),
                    included=bool(e.get("included", True)),
                )
                db.add(row)
            qty_user = e.get("qty_user")
            row.qty_user = float(qty_user) if qty_user not in (None, "") else None
            if "included" in e:
                row.included = bool(e["included"])
            if "notes" in e:
                row.notes = e.get("notes")
            row.updated_by = updated_by or row.updated_by
            count += 1
    return count


def log_ai_action(
    tenant_id: int,
    user_id: Optional[int],
    conversation_id: Optional[int],
    action: str,
    payload: Optional[dict] = None,
    status: str = "ok",
) -> None:
    with session_scope(tenant_id=tenant_id) as db:
        db.add(
            AIActionLog(
                tenant_id=tenant_id,
                user_id=user_id,
                conversation_id=conversation_id,
                action=action,
                payload=payload or {},
                status=status,
            )
        )


__all__ = [
    "upsert_inventory_snapshot",
    "upsert_sales_snapshot",
    "upsert_suggestions_from_analysis",
    "list_suggestions",
    "apply_suggestion_edits",
    "log_ai_action",
]
