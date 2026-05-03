"""Dashboard ejecutivo: KPIs, capital inmovilizado, alertas."""
from __future__ import annotations

import hashlib

import pandas as pd
import plotly.express as px
import streamlit as st

from core.auth import require_login
from core.access import can
from core.billing import has_active_access
from core.database import tenant_session_scope
from core.models import AnalysisRun, AuditLog
from engine import full_analysis
from engine.demo_data import get_demo_dataset
from engine.optimization import AnalysisConfig, simulate_service_level_impact
from services.inventory_store import (
    upsert_inventory_snapshot,
    upsert_sales_snapshot,
    upsert_suggestions_from_analysis,
)
from ui.components import format_currency, integration_banner, kpi, paywall, section_shell


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
    signature = hashlib.sha1(
        f"{tenant_id}|{len(df)}|{sales_rows}|{df['valor_inventario'].sum():.2f}|{df['capital_inmovilizado'].sum():.2f}".encode("utf-8")
    ).hexdigest()
    if st.session_state.get("_last_persisted_analysis_signature") == signature:
        return
    run_id: int | None = None
    try:
        with tenant_session_scope(tenant_id=tenant_id) as db:
            run = AnalysisRun(
                tenant_id=tenant_id,
                user_email=email,
                rows_inventory=int(len(df)),
                rows_sales=int(sales_rows),
                capital_total=float(df["valor_inventario"].sum()),
                capital_inmovilizado=float(df["capital_inmovilizado"].sum()),
            )
            db.add(run)
            db.add(
                AuditLog(
                    tenant_id=tenant_id,
                    user_email=email,
                    action="analysis_run",
                    entity="dashboard",
                    notes=f"rows_inventory={len(df)} rows_sales={sales_rows}",
                )
            )
            db.flush()
            run_id = run.id
        st.session_state["_last_persisted_analysis_signature"] = signature
    except Exception:
        pass

    # Snapshots persistentes y sugerencias UPSERT — solo si el plan lo habilita.
    user = st.session_state.get("auth") or {"tenant_id": tenant_id, "email": email}
    try:
        if user and can(user, "snapshots_persisted"):
            inv_df = st.session_state.get("uploaded_inventory")
            sales_df = st.session_state.get("uploaded_sales")
            if inv_df is not None:
                upsert_inventory_snapshot(tenant_id, inv_df)
            if sales_df is not None:
                upsert_sales_snapshot(tenant_id, sales_df)
            upsert_suggestions_from_analysis(tenant_id, df, run_id=run_id, updated_by=email)
    except Exception:
        pass


def _build_exec_summary(df: pd.DataFrame) -> tuple[str, str, list[str], int]:
    quiebres_a = int(((df["abc"] == "A") & (df["estado"] == "QUIEBRE")).sum())
    reponer_a = int(((df["abc"] == "A") & (df["estado"] == "REPONER")).sum())
    pct_inmov = float((df["capital_inmovilizado"].sum() / max(df["valor_inventario"].sum(), 1)) * 100)
    risk_score = min(100, int(quiebres_a * 14 + reponer_a * 6 + pct_inmov * 0.7))

    if risk_score >= 70:
        title = "Riesgo operativo alto"
        narrative = "Hay presión combinada en quiebres clase A, capital atrapado y reposición pendiente. La prioridad es proteger ventas y liberar caja rápida."
    elif risk_score >= 35:
        title = "Riesgo controlable con acción semanal"
        narrative = "El inventario ya muestra focos de presión, pero todavía hay margen para corregir compras, sobrestock y prioridades de surtido."
    else:
        title = "Salud operativa estable"
        narrative = "El inventario luce razonablemente controlado. El foco pasa a optimización fina, reducción de capital y disciplina de reposición."

    chips = [
        f"{int(df['sku'].nunique())} SKUs analizados",
        f"{int((df['estado'] == 'SOBRESTOCK').sum())} SKU con sobrestock",
        f"{int((df['capital_inmovilizado'] > 0).sum())} SKU con caja atrapada",
    ]
    return title, narrative, chips, risk_score


def render() -> None:
    user = require_login()
    if not has_active_access(user["tenant_id"]):
        paywall()
        return

    section_shell(
        "Bienvenido a OptiFerre",
        "El sistema que convierte inventario en decisiones: menos pérdidas, menos caja atrapada y compras más claras.",
        eyebrow="Golpe de valor",
    )
    st.markdown(
        """
        <div class='of-lead-panel'>
            <div class='of-lead-grid'>
                <div>
                    <div class='of-eyebrow'>Lo que deberías sentir en 5 segundos</div>
                    <h3>Este sistema existe para reducir pérdidas, proteger ventas y ayudarte a comprar mejor.</h3>
                    <p class='of-helper-line'>Si hoy tienes sobrestock, capital inmovilizado o compras hechas por intuición, aquí debería quedar claro qué está pasando y cuál es la siguiente acción.</p>
                </div>
                <div>
                    <div class='of-stat-line'><strong>Impacto esperado</strong><span>Menos dinero atrapado en productos lentos y menos quiebres en SKUs críticos.</span></div>
                    <div class='of-stat-line'><strong>Primer logro</strong><span>Detectar rápido el riesgo y bajar a una compra sugerida sin perderte en menús.</span></div>
                    <div class='of-stat-line'><strong>Prueba social honesta</strong><span>Equipos que usan herramientas similares suelen mejorar visibilidad de inventario desde el primer ciclo de revisión.</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("Flujo recomendado: 1. Carga de Datos  2. Insights IA  3. Qué Comprar. Si ya cargaste archivos, este tablero debería mostrarte el problema y la oportunidad de inmediato.")
    st.markdown(
        """
        <div class='of-lead-panel'>
            <div class='of-lead-grid'>
                <div>
                    <div class='of-eyebrow'>Qué debe pasar aquí</div>
                    <h3>Un gerente debe entender en menos de dos minutos dónde está el riesgo y qué acción sigue</h3>
                    <p class='of-helper-line'>Este dashboard no es un tablero decorativo. Debe traducir inventario en caja, urgencia, foco comercial y decisiones concretas que una empresa pueda ejecutar hoy.</p>
                </div>
                <div>
                    <div class='of-stat-line'><strong>Riesgo</strong><span>Quiebres, presión sobre clase A y riesgo de agotamiento.</span></div>
                    <div class='of-stat-line'><strong>Caja</strong><span>Capital atrapado y costo de oportunidad mensual.</span></div>
                    <div class='of-stat-line'><strong>Prioridad</strong><span>Tareas para proteger ventas y liberar capital.</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    df = _ensure_analysis()
    if df is None or df.empty:
        st.warning("Aún no has cargado datos. Empieza por **1. Carga de Datos** para desbloquear insights, IA y compra sugerida.")
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
    summary_title, summary_text, chips, risk_score = _build_exec_summary(df)

    action_cols = st.columns(3)
    action_cols[0].metric("Dinero atrapado en stock", format_currency(inmov))
    action_cols[1].metric("Productos en riesgo de quiebre", f"{quiebres:,}")
    action_cols[2].metric("SKUs a revisar hoy", f"{int((df['estado'] != 'OK').sum()):,}")

    st.markdown("### Pasos para el éxito")
    step_cols = st.columns(3)
    step_cols[0].info("1. Datos cargados. Si no confías en el resultado, vuelve a revisar la calidad de inventario y ventas.")
    step_cols[1].info("2. Deja que la IA analice. Este tablero resume el riesgo real de caja y disponibilidad.")
    step_cols[2].info("3. Ejecuta la compra sugerida. Lleva las prioridades a 3. Qué Comprar y genera la orden.")

    st.markdown(
        f"""
        <div class='of-exec-shell'>
            <div class='of-eyebrow'>{'Demo guiada activa' if st.session_state.get('demo_mode') else 'Diagnóstico con datos del tenant'}</div>
            <div class='of-exec-grid'>
                <div>
                    <h2 style='margin:8px 0 0 0'>{summary_title}</h2>
                    <p class='of-mini-note' style='margin-top:10px'>{summary_text}</p>
                    <div class='of-chip-row'>{''.join(f"<span class='of-chip'>{chip}</span>" for chip in chips)}</div>
                    <div class='of-metric-strip'>
                        <div class='of-metric-pill'>
                            <div class='caption'>Health Score</div>
                            <div class='value'>{max(0, 100 - risk_score)}/100</div>
                        </div>
                        <div class='of-metric-pill'>
                            <div class='caption'>Capital atrapado</div>
                            <div class='value'>{format_currency(inmov)}</div>
                        </div>
                        <div class='of-metric-pill'>
                            <div class='caption'>Caja sacrificada / mes</div>
                            <div class='value'>{format_currency(monthly_opp)}</div>
                        </div>
                    </div>
                </div>
                <div class='of-priority-card'>
                    <div class='of-eyebrow'>Qué haría un gerente hoy</div>
                    <ul class='of-priority-list'>
                        <li>Proteger los SKUs clase A en quiebre o bajo ROP.</li>
                        <li>Atacar primero el capital inmovilizado con mayor impacto mensual.</li>
                        <li>Revisar el nivel de servicio antes de sobrecomprar por reflejo.</li>
                    </ul>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    with cols[0]:
        kpi("Capital total", format_currency(capital))
    with cols[1]:
        kpi("Capital inmovilizado", format_currency(inmov), f"{pct_inmov:.1f}% del total")
    with cols[2]:
        kpi("SKUs en quiebre", f"{quiebres:,}", "Atención inmediata")
    with cols[3]:
        kpi("Costo oportunidad / mes", format_currency(monthly_opp), "Caja que no rota")

    if can(user, "advanced_dashboard"):
        st.caption("Insight IA desbloqueado: este diagnóstico ya está alimentando el centro de compra sugerida y el Asistente IA.")
    else:
        st.info("Tu plan actual te deja ver el diagnóstico base. Desbloquea el análisis explicado por IA para entender el porqué detrás de cada sugerencia.")

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

    spotlight_cols = st.columns(3)
    with spotlight_cols[0]:
        top_sobrestock = df.sort_values("capital_inmovilizado", ascending=False).head(1)
        top_name = top_sobrestock.iloc[0]["nombre_comercial"] if not top_sobrestock.empty else "Sin sobrestock crítico"
        top_value = float(top_sobrestock.iloc[0]["capital_inmovilizado"]) if not top_sobrestock.empty else 0
        kpi("Mayor foco de caja", top_name[:24], format_currency(top_value))
    with spotlight_cols[1]:
        panic_count = int(((df["demanda_diaria_avg"] > 0) & (df["stock_actual"] / df["demanda_diaria_avg"] <= 7)).sum())
        kpi("Riesgo 7 días", f"{panic_count:,}", "SKUs podrían agotarse")
    with spotlight_cols[2]:
        a_critical = int(((df["abc"] == "A") & (df["estado"].isin(["QUIEBRE", "REPONER"]))).sum())
        kpi("Clase A bajo presión", f"{a_critical:,}", "Prioridad comercial")

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
    fig4.update_traces(line_color="#10B7C4")
    fig4.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig4, use_container_width=True)

    best_level = scenarios.sort_values("costo_oportunidad_mensual").iloc[0]
    st.info(
        f"Escenario más liviano en caja dentro del simulador: {int(best_level['service_level'] * 100)}% de nivel de servicio, "
        f"con costo de oportunidad mensual estimado de {format_currency(float(best_level['costo_oportunidad_mensual']))}."
    )

    integration_banner()
