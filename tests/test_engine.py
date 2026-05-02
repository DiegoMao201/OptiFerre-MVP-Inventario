"""Tests mínimos para validar el motor de optimización."""
from __future__ import annotations

import math

import pandas as pd

from engine import full_analysis
from engine.optimization import (
    abc_classification,
    calculate_reorder_point,
    calculate_safety_stock,
    xyz_classification,
)


def test_safety_stock_basic():
    ss = calculate_safety_stock(avg_demand=10, lead_time=9, service_level=0.95)
    # Z=1.65, sigma=2 (20% de 10), sqrt(9)=3 -> 1.65*2*3 = 9.9 -> ceil=10
    assert ss == 10


def test_safety_stock_zero_demand():
    assert calculate_safety_stock(0, 5) == 0


def test_reorder_point():
    assert calculate_reorder_point(5, 4, 7) == math.ceil(5 * 4 + 7) == 27


def test_abc_classification():
    df = pd.DataFrame({"valor_inventario": [1000, 500, 100, 50, 10]})
    out = abc_classification(df)
    assert out.iloc[0] == "A"
    assert "C" in set(out)


def test_xyz_classification():
    cv = pd.Series([0.1, 0.6, 1.5])
    out = xyz_classification(cv)
    assert list(out) == ["X", "Y", "Z"]


def test_full_analysis_pipeline():
    inv = pd.DataFrame(
        [
            {"sku": "PHA046", "nombre_comercial": "Interthane 990", "stock_actual": 5,
             "costo_unitario": 100000, "lead_time_dias": 14, "categoria": "Quim",
             "unidad_empaque_minimo": 1},
            {"sku": "TOR1", "nombre_comercial": "Tornillo", "stock_actual": 1000,
             "costo_unitario": 100, "lead_time_dias": 7, "categoria": "Ferr",
             "unidad_empaque_minimo": 100},
        ]
    )
    sales = pd.DataFrame(
        [
            {"fecha": "2026-01-01", "sku": "PHA046", "cantidad_vendida": 2, "tipo_documento": "FV"},
            {"fecha": "2026-01-15", "sku": "PHA046", "cantidad_vendida": 1, "tipo_documento": "NC"},
            {"fecha": "2026-02-01", "sku": "TOR1", "cantidad_vendida": 250, "tipo_documento": "FV"},
        ]
    )
    df = full_analysis(inv, sales)
    assert {"abc", "xyz", "estado", "stock_seguridad", "punto_reorden", "sugerencia_compra"}.issubset(df.columns)
    # Catalizador detectado para Interthane
    row = df[df["sku"] == "PHA046"].iloc[0]
    assert row["catalizador_sugerido"] == "PHA046"
    # Sugerencia debe ser múltiplo del empaque mínimo
    tor = df[df["sku"] == "TOR1"].iloc[0]
    assert tor["sugerencia_compra"] % 100 == 0
