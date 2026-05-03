"""Página de planes y suscripción Stripe."""
from __future__ import annotations

import streamlit as st

from core.auth import require_login
from core.billing import PLAN_CATALOG, create_checkout_session, get_subscription
from core.plans import public_catalog
from core.config import get_settings
from ui.components import integration_banner, section_shell


def _plan_card(plan_key: str, info: dict, current_plan: str | None, user: dict) -> None:
    is_current = current_plan == plan_key
    border = "2px solid var(--primary)" if is_current else "1px solid var(--card-border)"
    badge = "<span class='of-pill'>Plan actual</span>" if is_current else ""
    feats = "".join(f"<li>{f}</li>" for f in info["features"])
    capabilities = "".join(
        f"<li><strong>Insight IA:</strong> {f}</li>" for f in info.get("ai_capabilities", [])[:3]
    )
    st.markdown(
        f"""
        <div style="background: var(--bg2); border: {border}; border-radius: 14px; padding: 18px 20px; height: 100%;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <h3 style='margin:0'>{info['name']}</h3>{badge}
          </div>
                    <div class='of-eyebrow' style='margin-top:6px'>{info.get('tagline','')}</div>
          <div style="font-size: 2rem; font-weight: 700; margin: 8px 0;">${info['price_monthly_usd']}<span style="font-size:.9rem; color:var(--muted)">/mes</span></div>
                    <p class='of-helper-line' style='margin:0 0 10px 0'>{info.get('summary','')}</p>
          <ul style="padding-left: 18px; line-height: 1.7;">{feats}</ul>
                    <ul style="padding-left: 18px; line-height: 1.7; margin-top:10px;">{capabilities}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Activar este plan" if not is_current else "Plan actualmente activo",
        key=f"btn_{plan_key}",
        use_container_width=True,
        disabled=is_current,
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
        "Comparación clara, upgrade en un clic y un mensaje directo de qué valor desbloquea cada plan.",
        eyebrow="Billing + crecimiento",
    )
    st.info("Starter te guía. Pro te explica dónde estás perdiendo dinero. Enterprise convierte ese análisis en automatización de órdenes y ejecución.")
    st.markdown(
        """
        <div class='of-lead-panel'>
            <div class='of-lead-grid'>
                <div>
                    <div class='of-eyebrow'>Compra con claridad</div>
                    <h3>Precios simples, activación inmediata y evolución por etapas</h3>
                    <p class='of-helper-line'>La suscripción cubre el uso continuo de la plataforma. Integraciones, multi-bodega avanzado o despliegue especial se cotizan aparte como servicios profesionales.</p>
                </div>
                <div>
                    <div class='of-stat-line'><strong>Trial</strong><span>Permite validar valor antes del primer pago.</span></div>
                    <div class='of-stat-line'><strong>Checkout</strong><span>La activación se hace por Stripe o demo local si Stripe no está listo.</span></div>
                    <div class='of-stat-line'><strong>Escalabilidad</strong><span>Puedes crecer de Starter a Enterprise sin rehacer el flujo.</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if sub:
        active = "🟢 Activa" if sub["is_active"] else "🔴 Inactiva"
        st.markdown(
            f"**Plan actual:** `{sub['plan'].upper()}` &nbsp;·&nbsp; **Estado:** {active}"
            + (f" &nbsp;·&nbsp; **Trial vence:** {sub['trial_ends_at']:%Y-%m-%d}"
               if sub["plan"] == "trial" and sub["trial_ends_at"] else "")
        )

    if not settings.stripe_enabled:
        st.warning(
            "⚠️ Stripe no está configurado (faltan claves en `.env`). "
            "Los botones activarán suscripciones en **modo demo** local para que puedas probar el flujo."
        )

    st.markdown("<div class='of-section-space'></div>", unsafe_allow_html=True)
    cols = st.columns(3)
    for col, (key, info) in zip(cols, public_catalog()):
        with col:
            _plan_card(key, info, sub["plan"] if sub else None, user)

    st.divider()
    integration_banner()
