"""Vista detallada del análisis: tabla con SS/ROP/sugerencia de compra y export."""
from __future__ import annotations

import io

import pandas as pd
import streamlit as st

from core.auth import require_login
from core.billing import has_active_access
from engine import full_analysis
from engine.optimization import AnalysisConfig, simulate_service_level_impact
from ui.components import integration_banner, paywall, section_shell

ESTADO_COLORS = {
    "QUIEBRE": "#E53935",
    "REPONER": "#FB8C00",
    "OK": "#43A047",
    "SOBRESTOCK": "#8E24AA",
}


def _highlight_estado(val: str) -> str:
    color = ESTADO_COLORS.get(val, "")
    return f"background-color: {color}; color: white; font-weight: 600;" if color else ""


def render() -> None:
    user = require_login()
    if not has_active_access(user["tenant_id"]):
        paywall()
        return

    section_shell(
        "Análisis detallado",
        "Aquí conviertes el modelo en decisiones revisables: filtras, comparas, exportas y bajas a SKU sin perder claridad.",
        eyebrow="Motor analítico",
    )
    inv = st.session_state.get("uploaded_inventory")
    sales = st.session_state.get("uploaded_sales")
    if inv is None or sales is None:
        st.warning("Carga tu inventario y ventas en **📤 Cargar Datos**.")
        return

    st.markdown(
        """
        <div class='of-lead-panel'>
            <div class='of-lead-grid'>
                <div>
                    <div class='of-eyebrow'>Lectura de decisión</div>
                    <h3>Filtra, recalcula y exporta sin perder el hilo ejecutivo</h3>
                    <p class='of-helper-line'>Esta vista existe para responder preguntas concretas: qué SKU está en quiebre, cuánto comprar, qué referencias tienen caja atrapada y cómo cambia la compra total si mueves el nivel de servicio.</p>
                </div>
                <div>
                    <div class='of-stat-line'><strong>Filtros</strong><span>Estado, ABC, XYZ y búsqueda por SKU o nombre.</span></div>
                    <div class='of-stat-line'><strong>Parámetros</strong><span>Puedes recalcular con otro service level y horizonte.</span></div>
                    <div class='of-stat-line'><strong>Exportación</strong><span>CSV o Excel con la tabla ya filtrada.</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("⚙️ Parámetros del modelo", expanded=False):
        cols = st.columns(3)
        sl = cols[0].select_slider(
            "Nivel de servicio",
            options=[0.90, 0.95, 0.975, 0.99],
            value=st.session_state.get("cfg_service_level", 0.95),
            format_func=lambda v: f"{int(v * 100)}%",
        )
        horizon = cols[1].slider("Horizonte de demanda (días)", 30, 365, st.session_state.get("cfg_horizon_days", 90), step=15)
        st.session_state["cfg_service_level"] = sl
        st.session_state["cfg_horizon_days"] = horizon
        if st.button("Recalcular", use_container_width=False):
            st.session_state.pop("analysis_result", None)

    df = st.session_state.get("analysis_result")
    if df is None:
        df = full_analysis(inv, sales, AnalysisConfig(service_level=sl, horizon_days=horizon))
        st.session_state["analysis_result"] = df

    cols = st.columns(4)
    estados = ["QUIEBRE", "REPONER", "OK", "SOBRESTOCK"]
    selected_estados = cols[0].multiselect("Estado", estados, default=estados)
    abc_opts = sorted(df["abc"].dropna().unique().tolist())
    selected_abc = cols[1].multiselect("ABC", abc_opts, default=abc_opts)
    xyz_opts = sorted(df["xyz"].dropna().unique().tolist())
    selected_xyz = cols[2].multiselect("XYZ", xyz_opts, default=xyz_opts)
    search = cols[3].text_input("🔎 Buscar SKU / nombre")

    filtered = df[
        df["estado"].isin(selected_estados)
        & df["abc"].isin(selected_abc)
        & df["xyz"].isin(selected_xyz)
    ]
    if search:
        s = search.upper()
        filtered = filtered[
            filtered["sku"].str.contains(s, na=False)
            | filtered["nombre_comercial"].str.upper().str.contains(s, na=False)
        ]

    show_cols = [
        "sku", "nombre_comercial", "categoria", "abc", "xyz", "clase", "estado",
        "stock_actual", "demanda_diaria_avg", "lead_time_dias",
        "stock_seguridad", "punto_reorden", "sugerencia_compra",
        "unidad_empaque_minimo", "catalizador_sugerido",
        "valor_inventario", "capital_inmovilizado", "dias_cobertura",
    ]
    show_cols = [c for c in show_cols if c in filtered.columns]
    view = filtered[show_cols].copy()
    view["dias_cobertura"] = view["dias_cobertura"].replace([float("inf")], 9999).round(1)
    view["demanda_diaria_avg"] = view["demanda_diaria_avg"].round(2)

    styled = view.style.applymap(_highlight_estado, subset=["estado"]) \
        .format({
            "valor_inventario": "${:,.0f}",
            "capital_inmovilizado": "${:,.0f}",
        })
    st.dataframe(styled, use_container_width=True, hide_index=True, height=520)

    st.markdown("#### Exportar resultados")
    scenarios = simulate_service_level_impact(inv, sales, horizon_days=horizon)
    current = scenarios[scenarios["service_level"] == sl]
    baseline = scenarios[scenarios["service_level"] == 0.95]
    if not current.empty and not baseline.empty:
        current_total = float(current.iloc[0]["sugerencia_compra_total"])
        base_total = float(baseline.iloc[0]["sugerencia_compra_total"])
        st.info(
            f"Con nivel de servicio {int(sl * 100)}%, la sugerencia total de compra es {current_total:,.0f} unidades. "
            f"Diferencia vs 95%: {current_total - base_total:,.0f}."
        )

    colx, coly = st.columns(2)
    csv_bytes = view.to_csv(index=False).encode("utf-8")
    colx.download_button(
        "⬇️ Descargar CSV",
        csv_bytes,
        file_name="optiferre_analisis.csv",
        mime="text/csv",
        use_container_width=True,
    )
    xls_buffer = io.BytesIO()
    with pd.ExcelWriter(xls_buffer, engine="xlsxwriter") as writer:
        view.to_excel(writer, index=False, sheet_name="Analisis")
    coly.download_button(
        "⬇️ Descargar Excel",
        xls_buffer.getvalue(),
        file_name="optiferre_analisis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    integration_banner()
