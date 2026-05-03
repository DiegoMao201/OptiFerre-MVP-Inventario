"""Carga de inventario y ventas."""
from __future__ import annotations

import io

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from api.deps.security import get_current_user
from engine.cleaning import clean_inventory, clean_sales
from services.inventory_store import (
    upsert_inventory_snapshot,
    upsert_sales_snapshot,
)

router = APIRouter()


def _read_table(file: UploadFile) -> pd.DataFrame:
    raw = file.file.read()
    if not raw:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "El archivo está vacío.")
    name = (file.filename or "").lower()
    try:
        if name.endswith(".csv") or file.content_type in {"text/csv", "application/csv"}:
            return pd.read_csv(io.BytesIO(raw))
        return pd.read_excel(io.BytesIO(raw))
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"No pudimos leer el archivo: {exc}") from exc


@router.post("/upload")
def upload_inventory(
    inventory: UploadFile = File(...),
    sales: UploadFile | None = File(None),
    current_user: dict = Depends(get_current_user),
) -> dict:
    inv_raw = _read_table(inventory)
    inv_clean = clean_inventory(inv_raw)
    inv_count = upsert_inventory_snapshot(current_user["tenant_id"], inv_clean)

    sales_count = 0
    sales_rows = 0
    if sales is not None:
        sales_raw = _read_table(sales)
        sales_clean = clean_sales(sales_raw)
        sales_rows = int(len(sales_clean))
        sales_count = upsert_sales_snapshot(current_user["tenant_id"], sales_clean)

    return {
        "ok": True,
        "inventory_rows": int(len(inv_clean)),
        "inventory_upserted": inv_count,
        "sales_rows": sales_rows,
        "sales_upserted": sales_count,
    }
