"""Página de descarga de plantillas."""
from __future__ import annotations

import streamlit as st

from core.templates import iter_templates
from ui.components import integration_banner


def render() -> None:
    st.markdown("## 📄 Plantillas oficiales")
    st.write(
        "Descarga estos archivos, complétalos con la información de tu empresa "
        "y súbelos en la sección **📤 Cargar Datos**. El sistema valida las columnas "
        "automáticamente."
    )
    st.markdown(
        """
        <div class='of-lead-panel'>
            <div class='of-lead-grid'>
                <div>
                    <div class='of-eyebrow'>Estructura oficial</div>
                    <h3>Plantillas pensadas para evitar ambigüedad desde el primer archivo</h3>
                    <p class='of-helper-line'>Cada plantilla deja claro qué columnas necesita la app para interpretar inventario, ventas o catálogos sin suposiciones. Esto reduce errores, acelera onboarding y transmite confianza comercial.</p>
                </div>
                <div>
                    <div class='of-stat-line'><strong>CSV</strong><span>Ideal para exportaciones rápidas desde ERP o Excel.</span></div>
                    <div class='of-stat-line'><strong>XLSX</strong><span>Útil cuando el cliente quiere revisar o completar manualmente.</span></div>
                    <div class='of-stat-line'><strong>Validación</strong><span>La app confirma columnas antes de permitir el análisis.</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for tpl in iter_templates():
        with st.container(border=True):
            st.markdown(f"### {tpl.title}")
            st.caption(tpl.description)
            required_columns = "".join(f"<span class='of-pill' style='margin:0 8px 8px 0; display:inline-flex'>{c}</span>" for c in tpl.required_columns)
            st.markdown(
                f"<div class='of-helper-line' style='margin:10px 0 14px 0'><strong style='color:var(--text)'>Columnas obligatorias:</strong> {required_columns}</div>",
                unsafe_allow_html=True,
            )
            st.dataframe(tpl.to_dataframe(), use_container_width=True, hide_index=True)
            cols = st.columns(2)
            with cols[0]:
                st.download_button(
                    label=f"⬇️ Descargar {tpl.title} (CSV)",
                    data=tpl.to_csv_bytes(),
                    file_name=f"plantilla_{tpl.key}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key=f"dl_csv_{tpl.key}",
                )
            with cols[1]:
                st.download_button(
                    label=f"⬇️ Descargar {tpl.title} (XLSX)",
                    data=tpl.to_xlsx_bytes(),
                    file_name=f"plantilla_{tpl.key}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key=f"dl_xlsx_{tpl.key}",
                )

    integration_banner()
