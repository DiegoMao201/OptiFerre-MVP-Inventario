"""Listados de productos: muertos y oportunidades."""
from __future__ import annotations

import math

import pandas as pd
from fastapi import APIRouter, Depends, Query

from api.deps.security import get_current_user
from api.schemas.dashboard import ProductList, ProductRow
from api.services.analysis_runner import latest_analysis


def _row_to_product(row: pd.Series) -> ProductRow:
    cobertura = row.get("dias_cobertura", 0)
    if cobertura is None or (isinstance(cobertura, float) and (math.isinf(cobertura) or math.isnan(cobertura))):
        cobertura = None
    return ProductRow(
        sku=str(row.get("sku", "")),
        nombre=str(row.get("nombre_comercial", row.get("sku", ""))),
        categoria=str(row.get("categoria", "")) or None,
        estado=str(row.get("estado", "")),
        stock_actual=float(row.get("stock_actual", 0) or 0),
        valor_inventario=float(row.get("valor_inventario", 0) or 0),
        dias_cobertura=float(cobertura) if cobertura is not None else None,
        sugerencia_compra=float(row.get("sugerencia_compra", 0) or 0),
        costo_oportunidad_mensual=float(row.get("costo_oportunidad_mensual", 0) or 0),
        abc=row.get("abc"),
        xyz=row.get("xyz"),
    )


def _empty_list() -> ProductList:
    return ProductList(items=[], total=0, total_value=0.0)


router = APIRouter()


@router.get("/dead", response_model=ProductList)
def dead_products(
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_user),
) -> ProductList:
    df = latest_analysis(current_user["tenant_id"])
    if df is None or df.empty:
        return _empty_list()
    mask = (df["estado"] == "SOBRESTOCK") | (df["demanda_diaria_avg"] == 0)
    subset = df.loc[mask].sort_values("valor_inventario", ascending=False).head(limit)
    items = [_row_to_product(r) for _, r in subset.iterrows()]
    return ProductList(
        items=items,
        total=int(mask.sum()),
        total_value=float(df.loc[mask, "valor_inventario"].sum()),
    )


@router.get("/opportunities", response_model=ProductList)
def opportunity_products(
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_user),
) -> ProductList:
    df = latest_analysis(current_user["tenant_id"])
    if df is None or df.empty:
        return _empty_list()
    mask = (df["sugerencia_compra"] > 0) | (df["estado"].isin(["QUIEBRE", "REPONER"]))
    subset = (
        df.loc[mask]
        .assign(
            _impacto=lambda d: d["sugerencia_compra"].astype(float)
            * d["costo_unitario"].astype(float)
        )
        .sort_values("_impacto", ascending=False)
        .head(limit)
    )
    items = [_row_to_product(r) for _, r in subset.iterrows()]
    return ProductList(
        items=items,
        total=int(mask.sum()),
        total_value=float((df.loc[mask, "sugerencia_compra"] * df.loc[mask, "costo_unitario"]).sum()),
    )


@router.get("/all", response_model=ProductList)
def all_products(
    limit: int = Query(500, ge=1, le=2000),
    current_user: dict = Depends(get_current_user),
) -> ProductList:
    df = latest_analysis(current_user["tenant_id"])
    if df is None or df.empty:
        return _empty_list()
    subset = df.sort_values("valor_inventario", ascending=False).head(limit)
    items = [_row_to_product(r) for _, r in subset.iterrows()]
    return ProductList(
        items=items,
        total=int(len(df)),
        total_value=float(df["valor_inventario"].sum()),
    )
