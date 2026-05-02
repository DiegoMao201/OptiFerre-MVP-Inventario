"""Datasets sintéticos para demo comercial y reducción de fricción."""
from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def build_demo_inventory() -> pd.DataFrame:
    rows = [
        ["TOR-1/2-G5", "Tornillo 1/2 Grado 5 caja x100", 240, 450, 7, "Ferreteria", 100],
        ["TOR-3/8-A2", "Tornillo inoxidable 3/8", 40, 1600, 15, "Ferreteria", 25],
        ["LIJ-150", "Lija agua #150", 800, 1200, 10, "Abrasivos", 50],
        ["DISCO-7", "Disco corte metal 7 pulg", 18, 3500, 12, "Abrasivos", 5],
        ["13227", "Catalizador Pintucoat", 6, 95000, 14, "Quimicos", 1],
        ["PHA046", "Catalizador Interthane 990", 2, 185000, 21, "Quimicos", 1],
        ["PINTUCOAT-BL", "Pintucoat Blanco Industrial", 14, 128000, 14, "Quimicos", 1],
        ["INTERTHANE-GR", "Interthane Gris", 3, 174000, 21, "Quimicos", 1],
        ["BROCA-12MM", "Broca industrial 12mm", 9, 28000, 18, "Herramientas", 1],
        ["SOLD-6013", "Electrodo 6013 caja", 120, 22000, 9, "Soldadura", 10],
    ]
    return pd.DataFrame(
        rows,
        columns=[
            "sku",
            "nombre_comercial",
            "stock_actual",
            "costo_unitario",
            "lead_time_dias",
            "categoria",
            "unidad_empaque_minimo",
        ],
    )


def build_demo_sales(days: int = 120) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    today = datetime.utcnow().date()
    skus = {
        "TOR-1/2-G5": 18,
        "TOR-3/8-A2": 5,
        "LIJ-150": 25,
        "DISCO-7": 4,
        "13227": 2,
        "PHA046": 1,
        "PINTUCOAT-BL": 3,
        "INTERTHANE-GR": 2,
        "BROCA-12MM": 1.5,
        "SOLD-6013": 10,
    }
    records: list[dict] = []
    for day_offset in range(days):
        current_date = today - timedelta(days=day_offset)
        for sku, mean in skus.items():
            qty = max(0, int(rng.normal(mean, max(1, mean * 0.35))))
            if qty == 0:
                continue
            records.append(
                {
                    "fecha": current_date.isoformat(),
                    "sku": sku,
                    "cantidad_vendida": qty,
                    "tipo_documento": "FV",
                }
            )
            if sku in {"13227", "PHA046"} and day_offset % 37 == 0:
                records.append(
                    {
                        "fecha": current_date.isoformat(),
                        "sku": sku,
                        "cantidad_vendida": 1,
                        "tipo_documento": "NC",
                    }
                )
    return pd.DataFrame(records)


def get_demo_dataset() -> tuple[pd.DataFrame, pd.DataFrame]:
    return build_demo_inventory(), build_demo_sales()