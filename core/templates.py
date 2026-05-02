"""Generador de plantillas CSV/XLSX para onboarding del cliente.

Cada plantilla expone (a) columnas obligatorias, (b) datos de ejemplo y
(c) helpers para descarga binaria desde Streamlit.
"""
from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class TemplateSpec:
    key: str
    title: str
    description: str
    required_columns: tuple[str, ...]
    sample_rows: list[dict]

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.sample_rows, columns=list(self.required_columns))

    def to_csv_bytes(self) -> bytes:
        return self.to_dataframe().to_csv(index=False).encode("utf-8")

    def to_xlsx_bytes(self) -> bytes:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            self.to_dataframe().to_excel(writer, index=False, sheet_name=self.key[:31])
        return buffer.getvalue()


INVENTORY_TEMPLATE = TemplateSpec(
    key="inventario",
    title="Inventario Maestro",
    description="Stock actual, costos y lead time por SKU.",
    required_columns=(
        "sku",
        "nombre_comercial",
        "stock_actual",
        "costo_unitario",
        "lead_time_dias",
        "categoria",
        "unidad_empaque_minimo",
    ),
    sample_rows=[
        {
            "sku": "PHA046",
            "nombre_comercial": "Catalizador Interthane 990",
            "stock_actual": 12,
            "costo_unitario": 185000,
            "lead_time_dias": 21,
            "categoria": "Quimicos",
            "unidad_empaque_minimo": 1,
        },
        {
            "sku": "13227",
            "nombre_comercial": "Catalizador Pintucoat",
            "stock_actual": 4,
            "costo_unitario": 95000,
            "lead_time_dias": 14,
            "categoria": "Quimicos",
            "unidad_empaque_minimo": 1,
        },
        {
            "sku": "TOR-1/2-G5",
            "nombre_comercial": "Tornillo 1/2 Grado 5 (caja x100)",
            "stock_actual": 320,
            "costo_unitario": 450,
            "lead_time_dias": 7,
            "categoria": "Ferreteria",
            "unidad_empaque_minimo": 100,
        },
    ],
)


SALES_TEMPLATE = TemplateSpec(
    key="ventas",
    title="Histórico de Ventas",
    description="Movimientos diarios. Las notas crédito (NC) se restan automáticamente.",
    required_columns=("fecha", "sku", "cantidad_vendida", "tipo_documento"),
    sample_rows=[
        {"fecha": "2026-01-15", "sku": "PHA046", "cantidad_vendida": 2, "tipo_documento": "FV"},
        {"fecha": "2026-01-22", "sku": "PHA046", "cantidad_vendida": 3, "tipo_documento": "FV"},
        {"fecha": "2026-01-28", "sku": "PHA046", "cantidad_vendida": 1, "tipo_documento": "NC"},
        {"fecha": "2026-02-03", "sku": "13227", "cantidad_vendida": 5, "tipo_documento": "FV"},
        {"fecha": "2026-02-10", "sku": "TOR-1/2-G5", "cantidad_vendida": 250, "tipo_documento": "FV"},
    ],
)


CATALOG_TEMPLATE = TemplateSpec(
    key="catalogo",
    title="Catálogo Maestro",
    description="Atributos comerciales del SKU (proveedor, marca, línea).",
    required_columns=(
        "sku",
        "nombre_comercial",
        "marca",
        "proveedor",
        "linea",
        "es_quimico",
    ),
    sample_rows=[
        {
            "sku": "PHA046",
            "nombre_comercial": "Catalizador Interthane 990",
            "marca": "International",
            "proveedor": "AkzoNobel",
            "linea": "Pinturas Industriales",
            "es_quimico": True,
        },
        {
            "sku": "13227",
            "nombre_comercial": "Catalizador Pintucoat",
            "marca": "Pintuco",
            "proveedor": "Pintuco S.A.",
            "linea": "Pinturas Industriales",
            "es_quimico": True,
        },
    ],
)


ALL_TEMPLATES: dict[str, TemplateSpec] = {
    INVENTORY_TEMPLATE.key: INVENTORY_TEMPLATE,
    SALES_TEMPLATE.key: SALES_TEMPLATE,
    CATALOG_TEMPLATE.key: CATALOG_TEMPLATE,
}


def validate_columns(df: pd.DataFrame, spec: TemplateSpec) -> tuple[bool, list[str]]:
    """Devuelve (ok, columnas_faltantes)."""
    missing = [c for c in spec.required_columns if c not in df.columns]
    return (len(missing) == 0, missing)


# ----- Helpers compatibles con la especificación original -----

def get_inventory_template() -> bytes:
    return INVENTORY_TEMPLATE.to_csv_bytes()


def get_sales_template() -> bytes:
    return SALES_TEMPLATE.to_csv_bytes()


def get_catalog_template() -> bytes:
    return CATALOG_TEMPLATE.to_csv_bytes()


def iter_templates() -> Iterable[TemplateSpec]:
    return ALL_TEMPLATES.values()
