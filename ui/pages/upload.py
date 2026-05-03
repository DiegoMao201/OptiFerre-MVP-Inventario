"""Carga y validación de archivos del cliente."""
from __future__ import annotations

import io

import pandas as pd
import streamlit as st

from core.templates import INVENTORY_TEMPLATE, SALES_TEMPLATE, validate_columns
from engine.cleaning import apply_smart_column_mapping
from engine.demo_data import get_demo_dataset
from ui.components import section_shell


def _read_any(uploaded) -> pd.DataFrame | None:
    if uploaded is None:
        return None
    name = uploaded.name.lower()
    data = uploaded.read()
    buffer = io.BytesIO(data)
    if name.endswith(".csv"):
        return pd.read_csv(buffer)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(buffer)
    raise ValueError("Formato no soportado. Usa CSV o XLSX.")


def render() -> None:
    section_shell(
        "Onboarding de datos",
        "Carga archivos reales o activa una demo guiada y obtén un diagnóstico ejecutivo en minutos.",
        eyebrow="Smart Importer + Demo Mode",
    )
    st.markdown(
        """
        <div class='of-lead-panel'>
            <div class='of-lead-grid'>
                <div>
                    <div class='of-eyebrow'>Carga sin fricción</div>
                    <h3>De Excel a diagnóstico accionable con una experiencia guiada y clara</h3>
                    <p class='of-helper-line'>Esta pantalla debe servirle a un cliente que llega con archivos imperfectos y necesita confiar rápido. Por eso cada bloque explica qué subir, qué valida la app y qué resultado obtiene al final.</p>
                </div>
                <div>
                    <div class='of-stat-line'><strong>1.</strong><span>Subes inventario y ventas en CSV o XLSX.</span></div>
                    <div class='of-stat-line'><strong>2.</strong><span>El sistema valida columnas y corrige aliases comunes.</span></div>
                    <div class='of-stat-line'><strong>3.</strong><span>Obtienes dashboard, análisis y compra sugerida.</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='of-upload-promo'>
            <div class='of-upload-promo-grid'>
                <div>
                    <h3 style='margin:0 0 8px 0'>Menos fricción, más tiempo a valor</h3>
                    <p class='of-mini-note' style='margin:0'>El Smart Importer reconoce aliases comunes de ERP y la demo guiada te deja mostrar valor comercial sin esperar la data del cliente.</p>
                    <div class='of-chip-row'>
                        <span class='of-chip'>Reconoce columnas ERP</span>
                        <span class='of-chip'>Corrige estructura antes del análisis</span>
                        <span class='of-chip'>Demo lista para vender</span>
                    </div>
                </div>
                <div>
                    <div class='of-upload-stat'>
                        <div class='of-eyebrow'>Resultado esperado</div>
                        <div style='font-size:1.2rem; font-weight:700; margin-top:6px'>Dashboard + ABC/XYZ + ROP + compra sugerida</div>
                        <p class='of-mini-note' style='margin:8px 0 0 0'>Puedes empezar con Excel y escalar a integración ERP después.</p>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    help_cols = st.columns(4)
    with help_cols[0]:
        with st.popover("¿Qué pasa con mis archivos?"):
            st.write(
                "Tus archivos se usan para validar estructura, limpiar datos y ejecutar el análisis de tu tenant actual."
            )
            st.write(
                "La idea del flujo es ayudarte a obtener recomendaciones sin obligarte a integrar ERP desde el primer día."
            )
    with help_cols[1]:
        with st.popover("¿Cómo sé qué columnas necesito?"):
            st.write(
                "La app valida columnas obligatorias contra las plantillas oficiales. Si algo falta, te lo indica antes del análisis."
            )
    with help_cols[2]:
        with st.popover("¿Se comparten mis datos?"):
            st.write(
                "No. El modelo es multitenant y cada empresa trabaja sobre su propia cuenta y su propia sesión de análisis."
            )
    with help_cols[3]:
        with st.popover("¿Qué obtengo después de subir?"):
            st.write(
                "Dashboard ejecutivo, clasificación ABC/XYZ, capital inmovilizado, stock de seguridad, ROP y sugerencia de compra exportable."
            )

    with st.expander("Ver guía rápida de carga y transparencia", expanded=False):
        st.markdown(
            """
            **Cómo funciona el proceso**

            1. Descargas o replicas la estructura de las plantillas oficiales.
            2. Subes inventario y ventas en CSV o Excel.
            3. El sistema revisa columnas mínimas, tipos y consistencia básica.
            4. Luego normaliza ventas, notas crédito y unidades para analizar mejor.
            5. El resultado se presenta en dashboard y tabla analítica exportable.

            **Transparencia sobre tus datos**

            - La información se usa para generar el análisis del tenant actual.
            - Las credenciales y configuración viven en la base de datos de la aplicación.
            - Los archivos deben cargarse con las columnas definidas para evitar ambigüedad.
            - Si deseas automatización ERP o integraciones continuas, eso se implementa como servicio adicional.
            """
        )

    st.markdown("<div class='of-section-space'></div>", unsafe_allow_html=True)
    cols = st.columns(2)
    with cols[0]:
        st.markdown("### 1) Inventario maestro")
        if st.button("Cargar demo guiada", use_container_width=True, key="load_demo_inventory"):
            demo_inventory, demo_sales = get_demo_dataset()
            st.session_state["uploaded_inventory"] = demo_inventory
            st.session_state["uploaded_sales"] = demo_sales
            st.session_state.pop("analysis_result", None)
            st.session_state["demo_mode"] = True
            st.success("Demo guiada cargada. Ya puedes ir a Dashboard o Análisis.")
        inv_file = st.file_uploader(
            "Inventario (CSV o XLSX)", type=["csv", "xlsx", "xls"], key="inv_uploader"
        )
        if inv_file is not None:
            try:
                df = _read_any(inv_file)
                df, mapping = apply_smart_column_mapping(df, schema="inventory")
                ok, missing = validate_columns(df, INVENTORY_TEMPLATE)
                if not ok:
                    st.error(f"❌ Faltan columnas obligatorias: {', '.join(missing)}")
                else:
                    st.session_state["uploaded_inventory"] = df
                    st.session_state.pop("analysis_result", None)
                    st.session_state["demo_mode"] = False
                    if mapping:
                        st.info(
                            "Smart Importer aplicó estas equivalencias: "
                            + ", ".join(f"{src} → {dst}" for src, dst in mapping.items())
                        )
                    st.success(f"✅ Inventario cargado: {len(df):,} filas.")
                    st.dataframe(df.head(10), use_container_width=True, hide_index=True)
            except Exception as exc:
                st.error(f"Error leyendo el archivo: {exc}")

    with cols[1]:
        st.markdown("### 2) Histórico de ventas")
        sales_file = st.file_uploader(
            "Ventas (CSV o XLSX)", type=["csv", "xlsx", "xls"], key="sales_uploader"
        )
        if sales_file is not None:
            try:
                df = _read_any(sales_file)
                df, mapping = apply_smart_column_mapping(df, schema="sales")
                ok, missing = validate_columns(df, SALES_TEMPLATE)
                if not ok:
                    st.error(f"❌ Faltan columnas obligatorias: {', '.join(missing)}")
                else:
                    st.session_state["uploaded_sales"] = df
                    st.session_state.pop("analysis_result", None)
                    st.session_state["demo_mode"] = False
                    if mapping:
                        st.info(
                            "Smart Importer aplicó estas equivalencias: "
                            + ", ".join(f"{src} → {dst}" for src, dst in mapping.items())
                        )
                    st.success(f"✅ Ventas cargadas: {len(df):,} filas.")
                    st.dataframe(df.head(10), use_container_width=True, hide_index=True)
            except Exception as exc:
                st.error(f"Error leyendo el archivo: {exc}")

    st.divider()
    inv_ready = "uploaded_inventory" in st.session_state
    sales_ready = "uploaded_sales" in st.session_state
    if inv_ready and sales_ready:
        st.success("🟢 Todo listo. Ve a **📊 Dashboard** o **🧠 Análisis** para ver los resultados.")
    else:
        st.info("Necesitas cargar **inventario** y **ventas** para ejecutar el análisis.")
