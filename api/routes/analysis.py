"""Ejecución del motor de análisis."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from api.deps.security import get_current_user
from api.schemas.dashboard import AnalysisRunResponse, DashboardSummary
from api.services.analysis_runner import run_analysis_for_tenant, summary_from_dataframe

router = APIRouter()


@router.post("/run", response_model=AnalysisRunResponse)
def run_analysis(
    service_level: float = 0.95,
    horizon_days: int = 90,
    current_user: dict = Depends(get_current_user),
) -> AnalysisRunResponse:
    out = run_analysis_for_tenant(
        current_user["tenant_id"],
        user_email=current_user["email"],
        service_level=service_level,
        horizon_days=horizon_days,
    )
    summary = summary_from_dataframe(out.get("result"))
    return AnalysisRunResponse(
        rows_inventory=out["rows_inventory"],
        rows_sales=out["rows_sales"],
        capital_total=out["capital_total"],
        capital_inmovilizado=out["capital_inmovilizado"],
        productos_muertos=out["productos_muertos"],
        summary=DashboardSummary(**summary),
    )
