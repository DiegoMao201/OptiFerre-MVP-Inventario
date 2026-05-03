from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class DashboardKPI(BaseModel):
    label: str
    value: float
    unit: str = "COP"
    hint: Optional[str] = None


class DashboardSummary(BaseModel):
    has_data: bool
    dinero_atrapado: float
    dinero_atrapado_mensual: float
    productos_muertos: int
    productos_muertos_valor: float
    productos_estrella: int
    en_quiebre: int
    para_reponer: int
    capital_total: float
    rotacion_promedio_dias: float


class ProductRow(BaseModel):
    sku: str
    nombre: str
    categoria: Optional[str] = None
    estado: str
    stock_actual: float
    valor_inventario: float
    dias_cobertura: Optional[float] = None
    sugerencia_compra: float = 0
    costo_oportunidad_mensual: float = 0
    abc: Optional[str] = None
    xyz: Optional[str] = None


class ProductList(BaseModel):
    items: list[ProductRow]
    total: int
    total_value: float


class AnalysisRunResponse(BaseModel):
    rows_inventory: int
    rows_sales: int
    capital_total: float
    capital_inmovilizado: float
    productos_muertos: int
    summary: DashboardSummary
