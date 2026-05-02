"""OptiFerre SaaS — punto de entrada Streamlit con routing dinámico multitenant."""
from __future__ import annotations

import streamlit as st

from core.auth import current_user, logout
from core.billing import get_subscription
from core.config import get_settings
from core.database import init_db
from core.tenancy import get_tenant
from ui.pages import (
    analysis,
    billing_page,
    dashboard,
    login,
    settings_page,
    templates_page,
    upload,
)
from ui.theme import inject_brand_css, render_brand_header

settings = get_settings()

st.set_page_config(
    page_title=settings.app_name,
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inicializar DB al arrancar
init_db()

# Tema base (puede ser sobrescrito por marca del tenant)
inject_brand_css("#FF6B1A", "dark")


PUBLIC_ROUTES = {
    "🔐 Acceso": login.render,
}

PRIVATE_ROUTES = {
    "📊 Dashboard": dashboard.render,
    "📤 Cargar Datos": upload.render,
    "🧠 Análisis": analysis.render,
    "📄 Plantillas": templates_page.render,
    "💳 Planes y Suscripción": billing_page.render,
    "🎨 Marca (White-label)": settings_page.render,
}


def _sidebar_user_block(user: dict) -> None:
    sub = get_subscription(user["tenant_id"])
    plan = sub["plan"].upper() if sub else "—"
    badge = "🟢" if (sub and sub["is_active"]) else "🔴"
    st.sidebar.markdown(
        f"""
        <div style="padding: 12px; border-radius: 12px; background: var(--bg2); border: 1px solid var(--card-border); margin-bottom: 12px;">
          <div style="font-weight:700;">{user['company_name']}</div>
          <div style="color: var(--muted); font-size:.85rem;">{user['email']}</div>
          <div style="margin-top:6px;"><span class='of-pill'>{badge} {plan}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    user = current_user()

    if user:
        # Aplicar branding del tenant
        tenant = get_tenant(user["tenant_id"])
        if tenant:
            inject_brand_css(tenant["brand_primary_color"], tenant["theme_mode"])
            render_brand_header(tenant["company_name"], tenant["brand_logo_url"])

        st.sidebar.title("OptiFerre SaaS")
        _sidebar_user_block(user)
        choice = st.sidebar.radio("Navegación", list(PRIVATE_ROUTES.keys()), label_visibility="collapsed")
        st.sidebar.divider()
        if st.sidebar.button("Cerrar sesión", use_container_width=True):
            logout()
            st.rerun()
        st.sidebar.caption(f"v0.1 · {settings.app_env}")

        PRIVATE_ROUTES[choice]()
    else:
        st.markdown(
            """
            <style>
              section[data-testid="stSidebar"] {display:none !important;}
              [data-testid="collapsedControl"] {display:none !important;}
            </style>
            """,
            unsafe_allow_html=True,
        )
        login.render()


if __name__ == "__main__":
    main()
