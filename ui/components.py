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


def format_currency(value: float, prefix: str = "$") -> str:
    try:
        return f"{prefix}{value:,.0f}"
    except Exception:
        return f"{prefix}0"
