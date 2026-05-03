"""Página de planes y suscripción Stripe."""
from __future__ import annotations

import streamlit as st

from core.auth import require_login
from core.billing import create_checkout_session, get_subscription
from core.plans import public_catalog
from core.config import get_settings
from ui.components import integration_banner, section_shell


PLAN_PITCH: dict[str, dict] = {
    "starter": {
        "headline": "Deja de adivinar",
        "for_who": "Para quien sube archivos sueltos y quiere orden YA",
        "you_get": [
            "Carga guiada con plantillas oficiales",
            "Smart Importer que entiende tu ERP",
            "Concierge IA que te dice qué hacer paso a paso",
            "Tickets y soporte por correo",
        ],
        "you_dont": "No incluye análisis profundo ni explicación IA por SKU.",
    },
    "pro": {
        "headline": "Libera tu caja",
        "for_who": "Para quien necesita saber qué productos le roban flujo de caja",
        "you_get": [
            "Todo lo de Starter",
            "Análisis ABC/XYZ explicado por IA en lenguaje humano",
            "Stock de seguridad y ROP justificados por SKU",
            "Snapshots persistentes para ver evolución",
            "Sugerencias de compra editables y guardadas",
        ],
        "you_dont": "No incluye generación de OC ni exportación profesional.",
    },
    "enterprise": {
        "headline": "Tu operación en piloto automático",
        "for_who": "Para quien quiere ejecutar, no solo analizar",
        "you_get": [
            "Todo lo de Pro",
            "Genera órdenes de compra reales en 1 clic",
            "Exportación profesional a Excel",
            "IA con function calling: ejecuta acciones",
            "White-label completo con tu marca",
            "Soporte prioritario",
        ],
        "you_dont": "Sin límites de SKUs ni usuarios.",
    },
}


def _plan_card(plan_key: str, info: dict, current_plan: str | None, user: dict) -> None:
    is_current = current_plan == plan_key
    pitch = PLAN_PITCH.get(plan_key, {})
    badge = "✓ Plan actual" if is_current else ""
    with st.container(border=True):
        cols = st.columns([3, 1])
        cols[0].markdown(f"### {info['name']}")
        if badge:
            cols[1].markdown(f"<div style='text-align:right'><span class='of-pill'>{badge}</span></div>", unsafe_allow_html=True)
        st.caption(info.get("tagline", ""))
        st.markdown(f"<div style='font-size:2.1rem;font-weight:800;margin:4px 0 2px 0;color:var(--text)'>${info['price_monthly_usd']}<span style='font-size:.9rem;color:var(--muted);font-weight:500'>/mes</span></div>", unsafe_allow_html=True)
        if pitch.get("headline"):
            st.markdown(f"**{pitch['headline']}**")
        if pitch.get("for_who"):
            st.caption(pitch["for_who"])
        st.markdown("**Qué obtienes:**")
        for f in pitch.get("you_get") or info.get("features", []):
            st.markdown(f"- {f}")
        if pitch.get("you_dont"):
            st.caption(f"ℹ️ {pitch['you_dont']}")
        if st.button(
            "Plan activo" if is_current else f"Activar {info['name']}",
            key=f"btn_{plan_key}",
            use_container_width=True,
            disabled=is_current,
            type="primary" if not is_current else "secondary",
        ):
            try:
                result = create_checkout_session(user["tenant_id"], user["email"], plan_key)
                if result.get("url"):
                    st.success("Redirigiendo a Stripe Checkout…")
                    st.link_button("Ir a Stripe →", result["url"], use_container_width=True)
                else:
                    st.info(result.get("message", "Suscripción activada en modo demo."))
                    st.rerun()
            except Exception as exc:
                st.error(f"No fue posible iniciar el checkout: {exc}")


def render() -> None:
    user = require_login()
    settings = get_settings()
    sub = get_subscription(user["tenant_id"])

    section_shell(
        "Planes y Suscripción",
        "Tres planes, una sola promesa: que veas dinero o ahorres tiempo en los próximos 60 segundos.",
        eyebrow="Elige tu nivel",
    )

    if sub:
        active = "🟢 Activa" if sub["is_active"] else "🔴 Inactiva"
        info_line = f"**Plan actual:** `{sub['plan'].upper()}` · **Estado:** {active}"
        if sub["plan"] == "trial" and sub.get("trial_ends_at"):
            info_line += f" · **Trial vence:** {sub['trial_ends_at']:%Y-%m-%d}"
        st.markdown(info_line)

    if not settings.stripe_enabled:
        st.warning(
            "⚠️ Stripe no está configurado. Los botones activan suscripciones en **modo demo** local para que pruebes el flujo end-to-end."
        )

    st.markdown("<div class='of-section-space'></div>", unsafe_allow_html=True)
    cols = st.columns(3)
    for col, (key, info) in zip(cols, public_catalog()):
        with col:
            _plan_card(key, info, sub["plan"] if sub else None, user)

    st.divider()
    integration_banner()
