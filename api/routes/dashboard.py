"""KPIs principales del dashboard ejecutivo."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from api.deps.security import get_current_user
from api.schemas.dashboard import DashboardSummary
from api.services.analysis_runner import latest_analysis, summary_from_dataframe

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def summary(current_user: dict = Depends(get_current_user)) -> DashboardSummary:
    df = latest_analysis(current_user["tenant_id"])
    return DashboardSummary(**summary_from_dataframe(df))
