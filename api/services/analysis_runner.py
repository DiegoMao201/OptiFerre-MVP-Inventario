"""Orquesta full_analysis a partir de los snapshots persistidos."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
from sqlalchemy import select

from core.database import session_scope, tenant_select
from core.models import AnalysisRun, InventorySnapshot, SalesSnapshot
from engine.optimization import AnalysisConfig, full_analysis
from services.inventory_store import upsert_suggestions_from_analysis


def _inventory_df(tenant_id: int) -> pd.DataFrame:
    with session_scope(tenant_id=tenant_id) as db:
        rows = db.scalars(tenant_select(db, InventorySnapshot)).all()
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(
            [
                {
                    "sku": r.sku,
                    "nombre_comercial": r.name or r.sku,
                    "categoria": r.category or "Sin categoria",
                    "stock_actual": float(r.on_hand or 0),
                    "costo_unitario": float(r.avg_cost or 0),
                    "lead_time_dias": float(r.lead_time_days or 7),
                    "unidad_empaque_minimo": float(r.pack_size or 1),
                }
                for r in rows
            ]
        )


def _sales_df(tenant_id: int, horizon_days: int = 90) -> pd.DataFrame:
    """Aproxima ventas diarias a partir de los snapshots agregados.

    Como SalesSnapshot guarda totales por período, distribuimos uniformemente
    sobre el rango para alimentar el motor de demanda.
    """
    with session_scope(tenant_id=tenant_id) as db:
        rows = db.scalars(tenant_select(db, SalesSnapshot)).all()
        if not rows:
            return pd.DataFrame(columns=["sku", "fecha", "cantidad_vendida", "tipo_documento"])

    expanded: list[dict] = []
    for r in rows:
        start = r.period_start
        end = r.period_end or (start + timedelta(days=1))
        days = max(1, (end - start).days)
        units = float(r.units_sold or 0)
        if units <= 0:
            continue
        per_day = units / days
        for d in range(days):
            expanded.append(
                {
                    "sku": r.sku,
                    "fecha": start + timedelta(days=d),
                    "cantidad_vendida": per_day,
                    "tipo_documento": "FV",
                }
            )
    if not expanded:
        return pd.DataFrame(columns=["sku", "fecha", "cantidad_vendida", "tipo_documento"])
    return pd.DataFrame(expanded)


def run_analysis_for_tenant(
    tenant_id: int,
    user_email: str,
    *,
    service_level: float = 0.95,
    horizon_days: int = 90,
) -> dict:
    inv = _inventory_df(tenant_id)
    if inv.empty:
        return {
            "rows_inventory": 0,
            "rows_sales": 0,
            "capital_total": 0.0,
            "capital_inmovilizado": 0.0,
            "productos_muertos": 0,
            "result": pd.DataFrame(),
        }
    sales = _sales_df(tenant_id, horizon_days=horizon_days)
    cfg = AnalysisConfig(service_level=service_level, horizon_days=horizon_days)
    result = full_analysis(inv, sales, cfg)

    capital_total = float(result["valor_inventario"].sum())
    capital_inmovilizado = float(result["capital_inmovilizado"].sum())
    productos_muertos = int((result["estado"] == "SOBRESTOCK").sum())

    with session_scope(tenant_id=tenant_id) as db:
        run = AnalysisRun(
            tenant_id=tenant_id,
            user_email=user_email,
            rows_inventory=int(len(inv)),
            rows_sales=int(len(sales)),
            capital_total=capital_total,
            capital_inmovilizado=capital_inmovilizado,
        )
        db.add(run)
        db.flush()
        run_id = run.id

    upsert_suggestions_from_analysis(
        tenant_id=tenant_id,
        df=result,
        run_id=run_id,
        updated_by=user_email,
    )

    return {
        "rows_inventory": int(len(inv)),
        "rows_sales": int(len(sales)),
        "capital_total": capital_total,
        "capital_inmovilizado": capital_inmovilizado,
        "productos_muertos": productos_muertos,
        "result": result,
    }


def latest_analysis(tenant_id: int) -> Optional[pd.DataFrame]:
    """Re-ejecuta el análisis si hay datos. (Stateless: el motor es rápido)."""
    out = run_analysis_for_tenant(tenant_id, user_email="system@optiferre.io")
    df = out.get("result")
    if df is None or df.empty:
        return None
    return df


def summary_from_dataframe(df: Optional[pd.DataFrame]) -> dict:
    if df is None or df.empty:
        return {
            "has_data": False,
            "dinero_atrapado": 0,
            "dinero_atrapado_mensual": 0,
            "productos_muertos": 0,
            "productos_muertos_valor": 0,
            "productos_estrella": 0,
            "en_quiebre": 0,
            "para_reponer": 0,
            "capital_total": 0,
            "rotacion_promedio_dias": 0,
        }
    muertos_mask = (df["estado"] == "SOBRESTOCK") | (df["demanda_diaria_avg"] == 0)
    estrellas_mask = (df.get("abc", "") == "A") & (df.get("xyz", "") == "X")
    rotacion_validos = df.loc[df["dias_cobertura"].notna() & (df["dias_cobertura"] != float("inf")), "dias_cobertura"]
    return {
        "has_data": True,
        "dinero_atrapado": float(df["capital_inmovilizado"].sum()),
        "dinero_atrapado_mensual": float(df["costo_oportunidad_mensual"].sum()),
        "productos_muertos": int(muertos_mask.sum()),
        "productos_muertos_valor": float(df.loc[muertos_mask, "valor_inventario"].sum()),
        "productos_estrella": int(estrellas_mask.sum()),
        "en_quiebre": int((df["estado"] == "QUIEBRE").sum()),
        "para_reponer": int((df["estado"] == "REPONER").sum()),
        "capital_total": float(df["valor_inventario"].sum()),
        "rotacion_promedio_dias": float(rotacion_validos.mean()) if not rotacion_validos.empty else 0.0,
    }


__all__ = ["run_analysis_for_tenant", "latest_analysis", "summary_from_dataframe"]
