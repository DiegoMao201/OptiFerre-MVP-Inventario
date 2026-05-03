"""Componentes reutilizables: KPIs, banners, paywall."""
from __future__ import annotations

import streamlit as st

from core.config import get_settings


def kpi(label: str, value: str, delta: str | None = None) -> None:
    delta_html = f"<div class='delta'>{delta}</div>" if delta else ""
    st.markdown(
        f"<div class='of-kpi'><div class='label'>{label}</div>"
        f"<div class='value'>{value}</div>{delta_html}</div>",
        unsafe_allow_html=True,
    )


def section_shell(title: str, subtitle: str | None = None, eyebrow: str | None = None) -> None:
    eyebrow_html = f"<div class='of-eyebrow'>{eyebrow}</div>" if eyebrow else ""
    subtitle_html = f"<p class='of-mini-note' style='margin:8px 0 0 0'>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"<div class='of-section-shell'>{eyebrow_html}<h3 style='margin:4px 0 0 0'>{title}</h3>{subtitle_html}</div>",
        unsafe_allow_html=True,
    )


def integration_banner() -> None:
    s = get_settings()
    st.markdown(
        f"""
        <div class='of-banner'>
          <h4>🔌 ¿Quieres conectar esto directamente a tu ERP (ICG, SAP, World Office, Siesa…)?</h4>
          <p>Este servicio de <b>integración personalizada</b> es modular y se cotiza por separado.
             <b>No está incluido</b> en la suscripción estándar.
             Escríbenos a <a href='mailto:{s.sales_email}'>{s.sales_email}</a> o llámanos al {s.sales_phone}.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def paywall(plan: str | None = None) -> None:
    st.error("🚫 Tu suscripción no está activa. Activa un plan para usar el motor de análisis.")
    st.markdown(
        "<div class='of-banner'><h4>Desbloquea OptiFerre</h4>"
        "<p>Activa tu plan en la sección <b>💳 Planes y Suscripción</b> y regresa aquí.</p></div>",
        unsafe_allow_html=True,
    )


def paywall_card(
    *,
    current_plan: str,
    required_plan: str,
    feature_key: str,
    title: str | None = None,
    description: str | None = None,
) -> None:
    """Paywall elegante para features bloqueadas por plan.

    No depende de session_state ni de Stripe; solo invita a ir a Planes.
    """
    from core.plans import plan_info  # diferido para evitar ciclos

    target = plan_info(required_plan) or {}
    target_name = target.get("name", required_plan.capitalize())
    tagline = target.get("tagline", "")
    bullets = target.get("ai_capabilities") or target.get("features") or []
    bullets_html = "".join(f"<li>{b}</li>" for b in bullets[:5])
    title = title or f"Esta función requiere el plan {target_name}"
    description = description or (
        f"Estás en el plan <b>{current_plan.upper()}</b>. "
        f"Sube a <b>{target_name}</b> para desbloquear esta capacidad ahora."
    )
    st.markdown(
        f"""
        <div class='of-paywall-card'>
            <div class='of-paywall-eyebrow'>Función bloqueada · {feature_key}</div>
            <h3 class='of-paywall-title'>{title}</h3>
            <p class='of-paywall-desc'>{description}</p>
            <div class='of-paywall-tagline'>{target_name} · {tagline}</div>
            <ul class='of-paywall-list'>{bullets_html}</ul>
            <div class='of-paywall-cta-row'>
                <span class='of-paywall-price'>${target.get('price_monthly_usd','—')}/mes</span>
                <span class='of-paywall-hint'>Activación inmediata desde Planes y Suscripción</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        f"Actualizar a {target_name} ahora",
        key=f"paywall_cta_{feature_key}",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["_jump_to_billing"] = True
        st.rerun()


def format_currency(value: float, prefix: str = "$") -> str:
    try:
        return f"{prefix}{value:,.0f}"
    except Exception:
        return f"{prefix}0"
