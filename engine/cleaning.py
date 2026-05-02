"""Limpieza financiera y normalización de datos provenientes de ERPs."""
from __future__ import annotations

from difflib import get_close_matches

import pandas as pd

# Documentos que SUMAN ventas reales
SALES_DOCS = {"FV", "FACTURA", "VENTA", "POS"}
# Documentos que RESTAN (devoluciones / notas crédito)
CREDIT_DOCS = {"NC", "NOTA_CREDITO", "DEVOLUCION", "RETURN"}

INVENTORY_COLUMN_ALIASES = {
    "sku": ["sku", "codigo", "cod", "referencia", "item", "producto"],
    "nombre_comercial": ["nombre", "descripcion", "descripcion producto", "producto", "nombre_producto"],
    "stock_actual": ["stock", "stock actual", "existencias", "qty", "cantidad", "inventario", "disponible"],
    "costo_unitario": ["costo", "costo unitario", "cost", "valor unitario", "costo promedio"],
    "lead_time_dias": ["lead time", "lead_time", "dias entrega", "plazo entrega", "lead time dias"],
    "categoria": ["categoria", "linea", "familia", "grupo"],
    "unidad_empaque_minimo": ["empaque", "unidad minima", "pack", "multiplo compra", "unidad_empaque"],
}

SALES_COLUMN_ALIASES = {
    "fecha": ["fecha", "date", "fecha venta", "fecha_documento"],
    "sku": ["sku", "codigo", "referencia", "item", "producto"],
    "cantidad_vendida": ["cantidad", "qty", "unidades", "cantidad vendida", "qty sold"],
    "tipo_documento": ["tipo documento", "documento", "tipo", "doc", "tipo_doc"],
}


def _coerce_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0)


def _normalize_column_name(value: str) -> str:
    return " ".join(str(value).strip().lower().replace("_", " ").split())


def suggest_column_mapping(df: pd.DataFrame, aliases: dict[str, list[str]]) -> dict[str, str]:
    """Sugiere y aplica un mapeo de columnas usando aliases y fuzzy matching."""
    normalized_columns = {col: _normalize_column_name(col) for col in df.columns}
    suggestions: dict[str, str] = {}
    used_targets: set[str] = set()

    for original, normalized in normalized_columns.items():
        exact_target = None
        for target, variants in aliases.items():
            vocabulary = {_normalize_column_name(target), *(_normalize_column_name(v) for v in variants)}
            if normalized in vocabulary:
                exact_target = target
                break
        if exact_target and exact_target not in used_targets:
            suggestions[original] = exact_target
            used_targets.add(exact_target)
            continue

        choices: dict[str, str] = {}
        for target, variants in aliases.items():
            for item in [target, *variants]:
                choices[_normalize_column_name(item)] = target

        match = get_close_matches(normalized, choices.keys(), n=1, cutoff=0.82)
        if match:
            target = choices[match[0]]
            if target not in used_targets:
                suggestions[original] = target
                used_targets.add(target)
    return suggestions


def apply_smart_column_mapping(df: pd.DataFrame, schema: str) -> tuple[pd.DataFrame, dict[str, str]]:
    aliases = INVENTORY_COLUMN_ALIASES if schema == "inventory" else SALES_COLUMN_ALIASES
    mapping = suggest_column_mapping(df, aliases)
    renamed = df.rename(columns=mapping)
    return renamed, mapping


def clean_inventory(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza el dataframe de inventario maestro."""
    df, _ = apply_smart_column_mapping(df.copy(), schema="inventory")
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
    df, _ = apply_smart_column_mapping(df.copy(), schema="sales")
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
