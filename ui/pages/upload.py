"""Carga y validación de archivos del cliente."""
from __future__ import annotations

import io

import pandas as pd
import streamlit as st

from core.templates import INVENTORY_TEMPLATE, SALES_TEMPLATE, validate_columns


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
    st.markdown("## 📤 Cargar datos")
    st.caption("Sube tu inventario y ventas. El motor procesa millones de filas en segundos.")

    cols = st.columns(2)
    with cols[0]:
        st.markdown("### 1) Inventario maestro")
        inv_file = st.file_uploader(
            "Inventario (CSV o XLSX)", type=["csv", "xlsx", "xls"], key="inv_uploader"
        )
        if inv_file is not None:
            try:
                df = _read_any(inv_file)
                ok, missing = validate_columns(df, INVENTORY_TEMPLATE)
                if not ok:
                    st.error(f"❌ Faltan columnas obligatorias: {', '.join(missing)}")
                else:
                    st.session_state["uploaded_inventory"] = df
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
                ok, missing = validate_columns(df, SALES_TEMPLATE)
                if not ok:
                    st.error(f"❌ Faltan columnas obligatorias: {', '.join(missing)}")
                else:
                    st.session_state["uploaded_sales"] = df
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
