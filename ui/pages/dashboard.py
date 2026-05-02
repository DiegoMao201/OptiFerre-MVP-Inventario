"""Dashboard ejecutivo: KPIs, capital inmovilizado, alertas."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from core.auth import require_login
from core.billing import has_active_access
from core.database import session_scope
from core.models import AnalysisRun
from engine import full_analysis
from engine.optimization import AnalysisConfig
from ui.components import format_currency, integration_banner, kpi, paywall


def _ensure_analysis() -> pd.DataFrame | None:
    if "analysis_result" in st.session_state:
        return st.session_state["analysis_result"]
    inv = st.session_state.get("uploaded_inventory")
    sales = st.session_state.get("uploaded_sales")
    if inv is None or sales is None:
        return None
    cfg = AnalysisConfig(
        service_level=st.session_state.get("cfg_service_level", 0.95),
        horizon_days=st.session_state.get("cfg_horizon_days", 90),
    )
    df = full_analysis(inv, sales, cfg)
    st.session_state["analysis_result"] = df
    return df


def _persist_run(tenant_id: int, email: str, df: pd.DataFrame, sales_rows: int) -> None:
    try:
        with session_scope() as db:
            db.add(
                AnalysisRun(
                    tenant_id=tenant_id,
                    user_email=email,
                    rows_inventory=int(len(df)),
                    rows_sales=int(sales_rows),
                    capital_total=float(df["valor_inventario"].sum()),
                    capital_inmovilizado=float(df["capital_inmovilizado"].sum()),
                )
            )
    except Exception:
        pass


def render() -> None:
    user = require_login()
    if not has_active_access(user["tenant_id"]):
        paywall()
        return

    st.markdown("## 📊 Dashboard ejecutivo")
    df = _ensure_analysis()
    if df is None or df.empty:
        st.warning("Aún no has cargado datos. Ve a **📤 Cargar Datos**.")
        return

    sales_rows = int(len(st.session_state.get("uploaded_sales", pd.DataFrame())))
    _persist_run(user["tenant_id"], user["email"], df, sales_rows)

    capital = float(df["valor_inventario"].sum())
    inmov = float(df["capital_inmovilizado"].sum())
    pct_inmov = (inmov / capital * 100) if capital else 0
    quiebres = int((df["estado"] == "QUIEBRE").sum())
    reponer = int((df["estado"] == "REPONER").sum())
    sobre = int((df["estado"] == "SOBRESTOCK").sum())

    cols = st.columns(4)
    with cols[0]:
        kpi("Capital total", format_currency(capital))
    with cols[1]:
        kpi("Capital inmovilizado", format_currency(inmov), f"{pct_inmov:.1f}% del total")
    with cols[2]:
        kpi("SKUs en quiebre", f"{quiebres:,}", "Atención inmediata")
    with cols[3]:
        kpi("SKUs por reponer", f"{reponer:,}", "Generar OC pronto")

    st.markdown("### 🔥 Alertas operativas")
    a, b, c = st.columns(3)
    a.metric("Quiebres", quiebres)
    b.metric("Por reponer", reponer)
    c.metric("Sobrestock", sobre)

    st.divider()
    st.markdown("### 💸 Top 10 capital inmovilizado")
    top_inmov = (
        df[df["capital_inmovilizado"] > 0]
        .sort_values("capital_inmovilizado", ascending=False)
        .head(10)
    )
    if top_inmov.empty:
        st.info("¡Excelente! No tienes capital inmovilizado relevante.")
    else:
        fig = px.bar(
            top_inmov,
            x="capital_inmovilizado",
            y="nombre_comercial",
            orientation="h",
            color="abc",
            text="capital_inmovilizado",
            labels={"capital_inmovilizado": "USD", "nombre_comercial": ""},
        )
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_layout(yaxis=dict(autorange="reversed"), height=420, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🧩 Distribución por clase ABC/XYZ")
    dist = df.groupby("clase", as_index=False).agg(skus=("sku", "count"), valor=("valor_inventario", "sum"))
    fig2 = px.treemap(dist, path=["clase"], values="valor", color="skus")
    fig2.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig2, use_container_width=True)

    integration_banner()
