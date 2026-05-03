"""OptiFerre SaaS — punto de entrada Streamlit con routing dinámico multitenant."""
from __future__ import annotations

import streamlit as st

from core.auth import current_user, logout
from core.billing import get_subscription
from core.config import get_settings
from core.database import init_db
from core.logging_config import clear_log_context, configure_logging, set_log_context
from core.tenancy import get_tenant
from ui.pages import (
    analysis,
    assistant,
    billing_page,
    dashboard,
    login,
    purchase_orders,
    settings_page,
    support_page,
    templates_page,
    upload,
)
from ui.theme import inject_brand_css, render_brand_header

settings = get_settings()
configure_logging()

st.set_page_config(
    page_title="OptiFerre",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inicializar DB al arrancar
init_db()

# Tema base inicial para la experiencia pública
inject_brand_css("#10B7C4", "dark")


PUBLIC_ROUTES = {
    "🔐 Acceso": login.render,
}

PRIVATE_ROUTES = {
    "📊 Dashboard": dashboard.render,
    "📤 Cargar Datos": upload.render,
    "🧠 Análisis": analysis.render,
    "� Órdenes de Compra": purchase_orders.render,
    "🤖 Asistente IA": assistant.render,
    "�📄 Plantillas": templates_page.render,
    "🆘 Soporte": support_page.render,
    "💳 Planes y Suscripción": billing_page.render,
    "🎨 Marca (White-label)": settings_page.render,
}


def _sidebar_user_block(user: dict) -> None:
    sub = get_subscription(user["tenant_id"])
    plan = sub["plan"].upper() if sub else "—"
    badge = "🟢" if (sub and sub["is_active"]) else "🔴"
    operator_emails = {settings.support_email.lower().strip(), settings.sales_email.lower().strip()}
    operator_badge = ""
    if user["email"].lower().strip() in operator_emails:
        operator_badge = "<div style='margin-top:8px; color:#0F6C7A; font-size:.82rem; font-weight:700;'>Operador habilitado: entra a Soporte para gestionar tickets globales</div>"
    st.sidebar.markdown(
        f"""
        <div style="padding: 12px; border-radius: 12px; background: var(--bg2); border: 1px solid var(--card-border); margin-bottom: 12px;">
          <div style="font-weight:700;">{user['company_name']}</div>
          <div style="color: var(--muted); font-size:.85rem;">{user['email']}</div>
          <div style="margin-top:6px;"><span class='of-pill'>{badge} {plan}</span></div>
          {operator_badge}
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    user = current_user()
    if user:
        set_log_context(tenant_id=user.get("tenant_id"), user_id=user.get("user_id"))
    else:
        clear_log_context()

    if user:
        # Aplicar branding del tenant
        tenant = get_tenant(user["tenant_id"])
        if tenant:
            inject_brand_css(tenant["brand_primary_color"], "light")
            render_brand_header(tenant["company_name"], tenant["brand_logo_url"])

        st.sidebar.title("OptiFerre")
        _sidebar_user_block(user)
        route_keys = list(PRIVATE_ROUTES.keys())
        default_idx = 0
        if st.session_state.pop("_jump_to_billing", False):
            for i, key in enumerate(route_keys):
                if "Planes" in key:
                    default_idx = i
                    break
        choice = st.sidebar.radio(
            "Navegación", route_keys, index=default_idx, label_visibility="collapsed"
        )
        st.sidebar.divider()
        if st.sidebar.button("Cerrar sesión", use_container_width=True):
            logout()
            st.rerun()
        st.sidebar.caption(f"v0.1 · {settings.app_env}")

        PRIVATE_ROUTES[choice]()
    else:
        inject_brand_css("#10B7C4", "dark")
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
