"""Motor global de optimización de inventarios.

Implementa:
* Métricas de demanda (promedio diario, sigma, CV).
* Clasificación ABC (Pareto por valor) y XYZ (previsibilidad).
* Stock de Seguridad dinámico con nivel de servicio configurable.
* Punto de Reorden (ROP).
* Guardarraíl industrial: redondeo math.ceil al empaque mínimo y
  sugerencia de catalizadores específicos para químicos.
* Pipeline `full_analysis` que une todo y devuelve el dataframe enriquecido.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from engine.cleaning import clean_inventory, clean_sales

# Z-scores comunes para nivel de servicio
SERVICE_LEVEL_Z = {
    0.90: 1.28,
    0.95: 1.65,
    0.975: 1.96,
    0.99: 2.33,
}

# Mapping de catalizadores específicos para químicos industriales.
# Si el inventario contiene la pintura base, el sistema sugiere su catalizador.
CHEMICAL_CATALYSTS = {
    "PINTUCOAT": "13227",
    "INTERTHANE": "PHA046",
}


@dataclass(frozen=True)
class AnalysisConfig:
    service_level: float = 0.95
    horizon_days: int = 90  # ventana para calcular demanda promedio
    abc_thresholds: tuple[float, float] = (0.80, 0.95)
    xyz_thresholds: tuple[float, float] = (0.5, 1.0)  # CV


# ---------- Métricas de demanda ----------

def build_demand_metrics(sales: pd.DataFrame, horizon_days: int = 90) -> pd.DataFrame:
    """Devuelve por SKU: demanda total, promedio diario, sigma diario y CV."""
    if sales.empty:
        return pd.DataFrame(
            columns=["sku", "demanda_total", "demanda_diaria_avg", "demanda_diaria_std", "cv"]
        )

    end_date = sales["fecha"].max().normalize()
    start_date = end_date - pd.Timedelta(days=horizon_days - 1)
    window = sales[sales["fecha"] >= start_date].copy()

    daily = (
        window.assign(fecha=window["fecha"].dt.normalize())
        .groupby(["sku", "fecha"], as_index=False)["cantidad_neta"]
        .sum()
    )

    # Re-indexar a calendario completo por SKU (días sin venta = 0)
    full_idx = pd.date_range(start_date, end_date, freq="D")
    pieces = []
    for sku, grp in daily.groupby("sku"):
        s = grp.set_index("fecha")["cantidad_neta"].reindex(full_idx, fill_value=0)
        pieces.append(pd.DataFrame({"sku": sku, "fecha": s.index, "qty": s.values}))
    if not pieces:
        return pd.DataFrame(
            columns=["sku", "demanda_total", "demanda_diaria_avg", "demanda_diaria_std", "cv"]
        )
    expanded = pd.concat(pieces, ignore_index=True)

    metrics = expanded.groupby("sku", as_index=False).agg(
        demanda_total=("qty", "sum"),
        demanda_diaria_avg=("qty", "mean"),
        demanda_diaria_std=("qty", "std"),
    )
    metrics["demanda_diaria_std"] = metrics["demanda_diaria_std"].fillna(0)
    metrics["cv"] = np.where(
        metrics["demanda_diaria_avg"] > 0,
        metrics["demanda_diaria_std"] / metrics["demanda_diaria_avg"],
        0,
    )
    return metrics


# ---------- Clasificaciones ----------

def abc_classification(df: pd.DataFrame, value_col: str = "valor_inventario",
                       thresholds: tuple[float, float] = (0.80, 0.95)) -> pd.Series:
    """Clasifica SKUs en A/B/C por Pareto sobre `value_col`."""
    if df.empty:
        return pd.Series(dtype=str)
    sorted_df = df.sort_values(value_col, ascending=False).copy()
    total = sorted_df[value_col].sum()
    if total <= 0:
        return pd.Series("C", index=df.index)
    sorted_df["acum"] = sorted_df[value_col].cumsum() / total
    a, b = thresholds

    def _cat(p: float) -> str:
        if p <= a:
            return "A"
        if p <= b:
            return "B"
        return "C"

    sorted_df["abc"] = sorted_df["acum"].apply(_cat)
    return sorted_df["abc"].reindex(df.index)


def xyz_classification(cv: pd.Series, thresholds: tuple[float, float] = (0.5, 1.0)) -> pd.Series:
    """X = predecible (CV<=0.5), Y = variable, Z = errático."""
    x, y = thresholds

    def _cat(v: float) -> str:
        if pd.isna(v) or v <= x:
            return "X"
        if v <= y:
            return "Y"
        return "Z"

    return cv.apply(_cat)


# ---------- Stock de seguridad y ROP ----------

def calculate_safety_stock(
    avg_demand: float,
    lead_time: float,
    service_level: float = 0.95,
    sigma: float | None = None,
) -> int:
    """SS = Z * sigma_d * sqrt(LT). Retorna entero (math.ceil).

    Si no se provee `sigma`, se asume variabilidad ≈ 20% de la demanda promedio
    (heurística conservadora para arranques sin histórico estable).
    """
    z = SERVICE_LEVEL_Z.get(round(service_level, 3), 1.65)
    sigma_d = sigma if sigma is not None else avg_demand * 0.2
    if avg_demand <= 0 or lead_time <= 0:
        return 0
    return math.ceil(z * sigma_d * math.sqrt(lead_time))


def calculate_reorder_point(avg_demand: float, lead_time: float, safety_stock: int) -> int:
    """ROP = demanda durante lead time + stock de seguridad."""
    return math.ceil(max(0.0, avg_demand) * max(0.0, lead_time) + max(0, safety_stock))


# ---------- Guardarraíl industrial ----------

def _round_to_pack(qty: float, pack: int) -> int:
    pack = max(1, int(pack or 1))
    if qty <= 0:
        return 0
    return int(math.ceil(qty / pack) * pack)


def apply_industrial_guardrails(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica redondeo a empaque mínimo y sugerencia de catalizadores."""
    out = df.copy()

    out["sugerencia_compra"] = [
        _round_to_pack(q, p)
        for q, p in zip(out["sugerencia_compra"], out["unidad_empaque_minimo"])
    ]

    # Sugerir catalizador según nombre/categoría
    def _catalyst(row: pd.Series) -> str:
        name = str(row.get("nombre_comercial", "")).upper()
        for keyword, sku in CHEMICAL_CATALYSTS.items():
            if keyword in name:
                return sku
        return ""

    out["catalizador_sugerido"] = out.apply(_catalyst, axis=1)
    return out


# ---------- Pipeline completo ----------

def full_analysis(
    inventory_df: pd.DataFrame,
    sales_df: pd.DataFrame,
    config: AnalysisConfig | None = None,
) -> pd.DataFrame:
    """Pipeline E2E: limpieza → métricas → SS/ROP → ABC/XYZ → guardarraíles."""
    cfg = config or AnalysisConfig()

    inv = clean_inventory(inventory_df)
    sales = clean_sales(sales_df)
    metrics = build_demand_metrics(sales, horizon_days=cfg.horizon_days)

    df = inv.merge(metrics, on="sku", how="left")
    for col in ("demanda_total", "demanda_diaria_avg", "demanda_diaria_std", "cv"):
        df[col] = df[col].fillna(0)

    # SS y ROP
    df["stock_seguridad"] = [
        calculate_safety_stock(
            avg_demand=row["demanda_diaria_avg"],
            lead_time=row["lead_time_dias"],
            service_level=cfg.service_level,
            sigma=row["demanda_diaria_std"] if row["demanda_diaria_std"] > 0 else None,
        )
        for _, row in df.iterrows()
    ]
    df["punto_reorden"] = [
        calculate_reorder_point(r["demanda_diaria_avg"], r["lead_time_dias"], r["stock_seguridad"])
        for _, r in df.iterrows()
    ]

    # Sugerencia de compra (déficit hasta cubrir ROP)
    df["sugerencia_compra"] = (df["punto_reorden"] - df["stock_actual"]).clip(lower=0)

    # Clasificaciones
    df["abc"] = abc_classification(df, "valor_inventario", cfg.abc_thresholds).fillna("C")
    df["xyz"] = xyz_classification(df["cv"], cfg.xyz_thresholds)
    df["clase"] = df["abc"] + df["xyz"]

    # Estado / alertas
    df["dias_cobertura"] = np.where(
        df["demanda_diaria_avg"] > 0, df["stock_actual"] / df["demanda_diaria_avg"], np.inf
    )
    df["capital_inmovilizado"] = np.where(
        (df["demanda_diaria_avg"] == 0) | (df["dias_cobertura"] > 180),
        df["valor_inventario"],
        0,
    )

    def _estado(row: pd.Series) -> str:
        if row["stock_actual"] <= 0:
            return "QUIEBRE"
        if row["stock_actual"] < row["punto_reorden"]:
            return "REPONER"
        if row["dias_cobertura"] > 180 or row["demanda_diaria_avg"] == 0:
            return "SOBRESTOCK"
        return "OK"

    df["estado"] = df.apply(_estado, axis=1)

    df = apply_industrial_guardrails(df)
    return df
