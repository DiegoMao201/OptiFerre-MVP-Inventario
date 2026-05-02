"""Página de Login + Registro de Tenants."""
from __future__ import annotations

import streamlit as st

from core.auth import authenticate, login, register_tenant


def render() -> None:
    st.markdown("## 🔐 Acceso a OptiFerre SaaS")
    tabs = st.tabs(["Iniciar sesión", "Crear cuenta (14 días gratis)"])

    with tabs[0]:
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email corporativo", placeholder="tu@empresa.com")
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Entrar", use_container_width=True)
        if submitted:
            data = authenticate(email, password)
            if data:
                login(data)
                st.success(f"Bienvenido, {data['full_name']} 👋")
                st.rerun()
            else:
                st.error("Credenciales inválidas.")

    with tabs[1]:
        with st.form("signup_form", clear_on_submit=False):
            company = st.text_input("Nombre de la ferretería / empresa")
            full_name = st.text_input("Tu nombre completo")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Contraseña (mín. 8)", type="password", key="signup_pwd")
            accept = st.checkbox("Acepto los términos y la política de privacidad.")
            submitted = st.form_submit_button("Crear cuenta", use_container_width=True)
        if submitted:
            if not all([company, full_name, email, password]) or len(password) < 8:
                st.error("Completa todos los campos. La contraseña debe tener al menos 8 caracteres.")
            elif not accept:
                st.error("Debes aceptar los términos.")
            else:
                try:
                    user = register_tenant(company, email, password, full_name)
                    data = authenticate(email, password)
                    if data:
                        login(data)
                        st.success("Cuenta creada. ¡Tienes 14 días de prueba gratis! 🎉")
                        st.rerun()
                except Exception as exc:  # pragma: no cover
                    st.error(f"No fue posible crear la cuenta: {exc}")
