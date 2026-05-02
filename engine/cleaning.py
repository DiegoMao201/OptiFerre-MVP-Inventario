"""Limpieza financiera y normalización de datos provenientes de ERPs."""
from __future__ import annotations

import pandas as pd

# Documentos que SUMAN ventas reales
SALES_DOCS = {"FV", "FACTURA", "VENTA", "POS"}
# Documentos que RESTAN (devoluciones / notas crédito)
CREDIT_DOCS = {"NC", "NOTA_CREDITO", "DEVOLUCION", "RETURN"}


def _coerce_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0)


def clean_inventory(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza el dataframe de inventario maestro."""
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    df["sku"] = df["sku"].astype(str).str.strip().str.upper()
    df["nombre_comercial"] = df["nombre_comercial"].astype(str).str.strip()
    df["categoria"] = df.get("categoria", "Sin categoria").astype(str).str.strip().replace("", "Sin categoria")

    df["stock_actual"] = _coerce_numeric(df["stock_actual"]).clip(lower=0)
    df["costo_unitario"] = _coerce_numeric(df["costo_unitario"]).clip(lower=0)
    df["lead_time_dias"] = _coerce_numeric(df.get("lead_time_dias", 7)).clip(lower=1)

    if "unidad_empaque_minimo" not in df.columns:
        df["unidad_empaque_minimo"] = 1
    df["unidad_empaque_minimo"] = _coerce_numeric(df["unidad_empaque_minimo"]).replace(0, 1)

    df = df.drop_duplicates(subset=["sku"], keep="last")
    df["valor_inventario"] = df["stock_actual"] * df["costo_unitario"]
    return df.reset_index(drop=True)


def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza ventas: parsea fechas, aplica signos por tipo de documento."""
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    df["sku"] = df["sku"].astype(str).str.strip().str.upper()
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df = df.dropna(subset=["fecha"])

    df["cantidad_vendida"] = _coerce_numeric(df["cantidad_vendida"])

    tipo = df.get("tipo_documento", "FV").astype(str).str.upper().str.strip()
    df["tipo_documento"] = tipo
    sign = tipo.apply(lambda t: -1 if t in CREDIT_DOCS else 1)
    df["cantidad_neta"] = df["cantidad_vendida"] * sign

    return df.reset_index(drop=True)
