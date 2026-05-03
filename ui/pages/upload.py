"""Carga y validación guiada de archivos del cliente."""
from __future__ import annotations

import io

import pandas as pd
import streamlit as st

from core.templates import ALL_TEMPLATES, CATALOG_TEMPLATE, INVENTORY_TEMPLATE, SALES_TEMPLATE, validate_columns
from engine.cleaning import apply_smart_column_mapping, clean_catalog
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


def render() -> None:
    section_shell(
        "Paso 1 · Sube tus datos",
        "Sube inventario y ventas. En segundos verás cuánto dinero está atrapado y qué deberías comprar primero.",
        eyebrow="Onboarding guiado",
    )
    st.markdown(
        """
        <div class='of-lead-panel'>
            <div class='of-lead-grid'>
                <div>
                    <div class='of-eyebrow'>Cómo funciona</div>
                    <h3>1. Sube tu archivo. 2. La IA analiza. 3. Decides qué comprar.</h3>
                    <p class='of-helper-line'>El Smart Importer reconoce los nombres de columnas más comunes de ERP. Si algo falta, te lo decimos en lenguaje claro y te damos la plantilla oficial para corregirlo.</p>
                </div>
                <div>
                    <div class='of-stat-line'><strong>Obligatorio</strong><span>Inventario maestro y ventas históricas.</span></div>
                    <div class='of-stat-line'><strong>Recomendado</strong><span>Catálogo maestro para ver proveedor, marca y línea.</span></div>
                    <div class='of-stat-line'><strong>Resultado</strong><span>Dashboard, ABC/XYZ, ROP y compra sugerida exportable.</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📥 Descargar plantillas oficiales y guía de columnas", expanded=False):
        st.caption(
            "Si tu ERP usa nombres distintos, el Smart Importer intentará mapearlos. Si falla, ajusta los encabezados a estas plantillas."
        )
        for tpl in ALL_TEMPLATES.values():
            st.markdown(f"**{tpl.title}** · {tpl.description}")
            required_columns = ", ".join(tpl.required_columns)
            st.caption(f"Columnas obligatorias: {required_columns}")
            preview = tpl.to_dataframe().head(3)
            st.dataframe(preview, use_container_width=True, hide_index=True)
            dl_cols = st.columns(2)
            dl_cols[0].download_button(
                f"⬇️ {tpl.title} · CSV",
                tpl.to_csv_bytes(),
                file_name=f"plantilla_{tpl.key}.csv",
                mime="text/csv",
                use_container_width=True,
                key=f"dl_inline_csv_{tpl.key}",
            )
            dl_cols[1].download_button(
                f"⬇️ {tpl.title} · XLSX",
                tpl.to_xlsx_bytes(),
                file_name=f"plantilla_{tpl.key}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key=f"dl_inline_xlsx_{tpl.key}",
            )
            st.divider()

    st.markdown("### Carga tus archivos")
    st.caption(
        "Inventario y ventas son obligatorios. El catálogo maestro es opcional pero recomendado: agrega proveedor, marca y línea a cada decisión."
    )

    st.markdown("<div class='of-section-space'></div>", unsafe_allow_html=True)
    cols = st.columns(3)
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

    with cols[2]:
        st.markdown("### 3) Catálogo maestro")
        st.caption("Opcional, pero recomendado. Agrega marca, proveedor y línea para que la lectura comercial sea más clara.")
        catalog_file = st.file_uploader(
            "Catálogo maestro (CSV o XLSX)", type=["csv", "xlsx", "xls"], key="catalog_uploader"
        )
        if catalog_file is not None:
            try:
                df = _read_any(catalog_file)
                df, mapping = apply_smart_column_mapping(df, schema="catalog")
                ok, missing = validate_columns(df, CATALOG_TEMPLATE)
                if not ok:
                    st.error(_human_validation_error("catálogo maestro", missing, CATALOG_TEMPLATE.title))
                else:
                    cleaned = clean_catalog(df)
                    st.session_state["uploaded_catalog"] = cleaned
                    if mapping:
                        st.info(
                            "Smart Importer aplicó estas equivalencias: "
                            + ", ".join(f"{src} → {dst}" for src, dst in mapping.items())
                        )
                    st.success(
                        f"✅ Catálogo maestro cargado: {len(cleaned):,} filas. La app ya tiene más contexto comercial para explicar mejor los resultados."
                    )
                    st.dataframe(cleaned.head(10), use_container_width=True, hide_index=True)
            except Exception:
                st.error(
                    "No pude procesar ese catálogo maestro. Revisa que incluya SKU, nombre comercial, marca, proveedor, línea y el indicador de si es químico."
                )

    st.divider()
    inv_ready = "uploaded_inventory" in st.session_state
    sales_ready = "uploaded_sales" in st.session_state
    catalog_ready = "uploaded_catalog" in st.session_state
    if inv_ready and sales_ready:
        if catalog_ready:
            st.success("🟢 Todo listo. Inventario, ventas y catálogo maestro ya están cargados. Siguiente paso recomendado: entra a **2. Insights IA** y luego a **3. Qué Comprar**.")
        else:
            st.success("🟢 Todo listo. Inventario y ventas ya están cargados. Si quieres una lectura más comercial, añade también catálogo maestro antes de ir a **2. Insights IA**.")
    else:
        st.info("Para obtener recomendaciones reales necesitas cargar al menos **inventario** y **ventas**. El **catálogo maestro** ya se puede cargar aquí y ayuda a enriquecer el contexto comercial.")
