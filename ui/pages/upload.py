"""Carga y validación guiada de archivos del cliente."""
from __future__ import annotations

import io

import pandas as pd
import streamlit as st

from core.templates import ALL_TEMPLATES, INVENTORY_TEMPLATE, SALES_TEMPLATE, validate_columns
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


def _human_validation_error(file_label: str, missing: list[str], template_key: str) -> str:
    missing_text = ", ".join(missing)
    return (
        f"No pude entender el archivo de {file_label} porque faltan estas columnas: {missing_text}. "
        f"Descarga la plantilla oficial de {template_key}, compara los encabezados y vuelve a subirlo. "
        "Si tu ERP usa otros nombres, el sistema intentará mapearlos automáticamente, pero la estructura base debe existir."
    )


def _render_template_hub() -> None:
    st.markdown("### Plantillas oficiales en el mismo flujo")
    st.info(
        "Todo empieza aquí. Descarga la plantilla correcta, completa tus datos y súbelos en esta misma pantalla. "
        "No necesitas salir a otra página para entender qué archivo usar."
    )
    for tpl in ALL_TEMPLATES.values():
        with st.expander(f"{tpl.title} · {tpl.description}", expanded=False):
            required_columns = ", ".join(tpl.required_columns)
            st.caption(f"Columnas obligatorias: {required_columns}")
            preview = tpl.to_dataframe().head(3)
            st.dataframe(preview, use_container_width=True, hide_index=True)
            dl_cols = st.columns(2)
            dl_cols[0].download_button(
                f"Descargar {tpl.title} CSV",
                tpl.to_csv_bytes(),
                file_name=f"plantilla_{tpl.key}.csv",
                mime="text/csv",
                use_container_width=True,
                key=f"dl_inline_csv_{tpl.key}",
            )
            dl_cols[1].download_button(
                f"Descargar {tpl.title} XLSX",
                tpl.to_xlsx_bytes(),
                file_name=f"plantilla_{tpl.key}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key=f"dl_inline_xlsx_{tpl.key}",
            )


def render() -> None:
    section_shell(
        "Paso 1 · Carga de datos",
        "Esta es la puerta de entrada: aquí entiendes qué archivos usar, cómo corregirlos y qué resultado obtendrás después.",
        eyebrow="Onboarding guiado",
    )
    st.markdown(
        """
        <div class='of-lead-panel'>
            <div class='of-lead-grid'>
                <div>
                    <div class='of-eyebrow'>Pasos para el éxito</div>
                    <h3>1. Carga tus datos. 2. Deja que la IA analice. 3. Ejecuta tu primera compra optimizada.</h3>
                    <p class='of-helper-line'>OptiFerre existe para reducir pérdidas por sobrestock y quiebres antes de que se conviertan en caja atrapada. Si hoy solo haces una cosa, empieza por subir inventario y ventas aquí.</p>
                </div>
                <div>
                    <div class='of-stat-line'><strong>Qué resuelve</strong><span>Te dice qué comprar, qué está drenando caja y qué puede dejarte sin ventas.</span></div>
                    <div class='of-stat-line'><strong>Para quién</strong><span>Dueños, compradores y gerentes de ferretería o distribución industrial.</span></div>
                    <div class='of-stat-line'><strong>Qué sigue</strong><span>Después de cargar, la app te lleva a insights y luego a compra sugerida.</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "Beneficio inmediato: en menos de unos minutos deberías ver dinero atrapado en stock, SKUs en riesgo y una compra sugerida priorizada."
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

    _render_template_hub()

    st.markdown("<div class='of-section-space'></div>", unsafe_allow_html=True)
    cols = st.columns(2)
    with cols[0]:
        st.markdown("### 1) Inventario maestro")
        st.caption("Base para saber cuánto stock tienes, cuánto cuesta y cuánto tarda en reponerse.")
        if st.button("Cargar demo guiada", use_container_width=True, key="load_demo_inventory"):
            demo_inventory, demo_sales = get_demo_dataset()
            st.session_state["uploaded_inventory"] = demo_inventory
            st.session_state["uploaded_sales"] = demo_sales
            st.session_state.pop("analysis_result", None)
            st.session_state["demo_mode"] = True
            st.success("Demo guiada cargada. Siguiente paso recomendado: entra a 2. Insights IA.")
        inv_file = st.file_uploader(
            "Inventario (CSV o XLSX)", type=["csv", "xlsx", "xls"], key="inv_uploader"
        )
        if inv_file is not None:
            try:
                df = _read_any(inv_file)
                df, mapping = apply_smart_column_mapping(df, schema="inventory")
                ok, missing = validate_columns(df, INVENTORY_TEMPLATE)
                if not ok:
                    st.error(_human_validation_error("inventario", missing, INVENTORY_TEMPLATE.title))
                else:
                    st.session_state["uploaded_inventory"] = df
                    st.session_state.pop("analysis_result", None)
                    st.session_state["demo_mode"] = False
                    if mapping:
                        st.info(
                            "Smart Importer aplicó estas equivalencias: "
                            + ", ".join(f"{src} → {dst}" for src, dst in mapping.items())
                        )
                    st.success(f"✅ Inventario cargado: {len(df):,} filas. Ya tenemos la base para calcular stock óptimo.")
                    st.dataframe(df.head(10), use_container_width=True, hide_index=True)
            except Exception as exc:
                st.error(
                    "No pude procesar ese archivo de inventario. Revisa que sea CSV o XLSX, que la primera fila tenga encabezados y que no venga exportado con celdas fusionadas."
                )

    with cols[1]:
        st.markdown("### 2) Histórico de ventas")
        st.caption("Es la señal que usa la IA para detectar rotación, reposición y riesgo de quiebre.")
        sales_file = st.file_uploader(
            "Ventas (CSV o XLSX)", type=["csv", "xlsx", "xls"], key="sales_uploader"
        )
        if sales_file is not None:
            try:
                df = _read_any(sales_file)
                df, mapping = apply_smart_column_mapping(df, schema="sales")
                ok, missing = validate_columns(df, SALES_TEMPLATE)
                if not ok:
                    st.error(_human_validation_error("ventas", missing, SALES_TEMPLATE.title))
                else:
                    st.session_state["uploaded_sales"] = df
                    st.session_state.pop("analysis_result", None)
                    st.session_state["demo_mode"] = False
                    if mapping:
                        st.info(
                            "Smart Importer aplicó estas equivalencias: "
                            + ", ".join(f"{src} → {dst}" for src, dst in mapping.items())
                        )
                    st.success(f"✅ Ventas cargadas: {len(df):,} filas. Ya podemos identificar rotación y urgencias de compra.")
                    st.dataframe(df.head(10), use_container_width=True, hide_index=True)
            except Exception as exc:
                st.error(
                    "No pude procesar ese archivo de ventas. Asegúrate de subir un CSV o XLSX con fechas, SKU, cantidad vendida y tipo de documento."
                )

    st.divider()
    inv_ready = "uploaded_inventory" in st.session_state
    sales_ready = "uploaded_sales" in st.session_state
    if inv_ready and sales_ready:
        st.success("🟢 Todo listo. Siguiente paso recomendado: entra a **2. Insights IA** para ver dónde estás perdiendo dinero y luego a **3. Qué Comprar** para ejecutar tu primera orden.")
    else:
        st.info("Para obtener recomendaciones reales necesitas cargar al menos **inventario** y **ventas**. El catálogo maestro es opcional, pero ayuda a enriquecer el contexto comercial.")
