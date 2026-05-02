"""Dashboard ejecutivo: KPIs, capital inmovilizado, alertas."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from core.auth import require_login
from core.billing import has_active_access
from core.database import tenant_session_scope
from core.models import AnalysisRun, AuditLog
from engine import full_analysis
from engine.demo_data import get_demo_dataset
from engine.optimization import AnalysisConfig, simulate_service_level_impact
from ui.components import format_currency, integration_banner, kpi, paywall


def _ensure_analysis() -> pd.DataFrame | None:
    if "analysis_result" in st.session_state:
        return st.session_state["analysis_result"]
    inv = st.session_state.get("uploaded_inventory")
    sales = st.session_state.get("uploaded_sales")
    if st.session_state.get("demo_mode") and (inv is None or sales is None):
        inv, sales = get_demo_dataset()
        st.session_state["uploaded_inventory"] = inv
        st.session_state["uploaded_sales"] = sales
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
        with tenant_session_scope(tenant_id=tenant_id) as db:
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
            db.add(
                AuditLog(
                    tenant_id=tenant_id,
                    user_email=email,
                    action="analysis_run",
                    entity="dashboard",
                    notes=f"rows_inventory={len(df)} rows_sales={sales_rows}",
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
    monthly_opp = float(df["costo_oportunidad_mensual"].sum())
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
        kpi("Costo oportunidad / mes", format_currency(monthly_opp), "Caja que no rota")

    st.markdown("### 🔥 Alertas operativas")
    a, b, c = st.columns(3)
    a.metric("Quiebres", quiebres)
    b.metric("Por reponer", reponer)
    c.metric("Sobrestock", sobre)

    st.markdown("### ✅ Tareas prioritarias")
    tasks = []
    critical = df[(df["abc"] == "A") & (df["estado"] == "QUIEBRE")]
    if not critical.empty:
        tasks.append(f"{len(critical)} SKUs clase A están en quiebre: generar pedido ya.")
    urgent = df[(df["abc"] == "A") & (df["estado"] == "REPONER")]
    if not urgent.empty:
        tasks.append(f"{len(urgent)} SKUs clase A están por debajo del ROP: revisar abastecimiento hoy.")
    trapped = df[df["capital_inmovilizado"] > 0].sort_values("capital_inmovilizado", ascending=False).head(3)
    if not trapped.empty:
        tasks.append(
            "Capital atrapado prioritario en: " + ", ".join(trapped["sku"].tolist()) + "."
        )
    panic = df[(df["demanda_diaria_avg"] > 0) & (df["stock_actual"] / df["demanda_diaria_avg"] <= 7)]
    if not panic.empty:
        tasks.append(f"Botón de pánico: {len(panic)} SKUs podrían agotarse en 7 días o menos.")
    for task in tasks or ["No hay alertas críticas inmediatas. Mantén seguimiento semanal."]:
        st.markdown(f"- {task}")

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

    st.markdown("### 🎯 Matriz de reducción de riesgo ABC/XYZ")
    bubble = df.copy()
    bubble["capital_plot"] = bubble["capital_inmovilizado"].clip(lower=1)
    fig3 = px.scatter(
        bubble,
        x="abc",
        y="xyz",
        size="capital_plot",
        color="estado",
        hover_name="nombre_comercial",
        hover_data={"sku": True, "capital_inmovilizado": ':,.0f', "costo_oportunidad_mensual": ':,.0f'},
        size_max=50,
    )
    fig3.update_layout(height=420, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### 🧪 Impacto del nivel de servicio")
    scenarios = simulate_service_level_impact(
        st.session_state.get("uploaded_inventory"),
        st.session_state.get("uploaded_sales"),
        horizon_days=st.session_state.get("cfg_horizon_days", 90),
    )
    fig4 = px.line(
        scenarios,
        x="service_level",
        y="sugerencia_compra_total",
        markers=True,
        hover_data={"capital_inmovilizado": ':,.0f', "costo_oportunidad_mensual": ':,.0f'},
    )
    fig4.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig4, use_container_width=True)

    integration_banner()
