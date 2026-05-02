"""Configuración white-label del tenant: marca, color, logo, modo."""
from __future__ import annotations

import streamlit as st

from core.auth import require_login
from core.tenancy import get_tenant, update_brand


def render() -> None:
    user = require_login()
    tenant = get_tenant(user["tenant_id"])
    if not tenant:
        st.error("No se encontró el tenant.")
        return

    st.markdown("## 🎨 Marca y apariencia")
    st.caption("Cada empresa cliente ve la app con sus propios colores, logo y nombre comercial.")

    with st.form("brand_form"):
        company = st.text_input("Nombre comercial", tenant["company_name"])
        color = st.color_picker("Color primario", tenant["brand_primary_color"])
        logo = st.text_input("URL del logo (https://…)", tenant["brand_logo_url"] or "")
        mode = st.selectbox(
            "Modo de tema", ["dark", "light"],
            index=0 if tenant["theme_mode"] == "dark" else 1,
        )
        submitted = st.form_submit_button("Guardar cambios", use_container_width=True)
    if submitted:
        update_brand(
            tenant_id=tenant["id"],
            company_name=company,
            primary_color=color,
            logo_url=logo,
            theme_mode=mode,
        )
        # Actualizar sesión para refrescar header
        st.session_state["auth"]["company_name"] = company
        st.success("Cambios guardados. Refrescando…")
        st.rerun()
