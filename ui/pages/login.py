"""Página de Login + Registro de Tenants."""
from __future__ import annotations

import streamlit as st

from core.billing import PLAN_CATALOG
from core.auth import authenticate, login, register_tenant


def _render_hero() -> None:
        st.markdown(
                """
                <div class='of-hero'>
                    <div class='of-eyebrow'>SaaS B2B para ferretería e industria</div>
                    <h1>Convierte inventario lento en decisiones rentables.</h1>
                    <p>
                        OptiFerre SaaS revela dónde tienes capital atrapado, qué SKUs están por romper stock
                        y cuánto deberías comprar realmente. Subes archivos, obtienes diagnóstico ejecutivo
                        y conviertes la intuición en decisiones de compra sostenibles.
                    </p>

                    <div class='of-proof'>
                        <div class='item'>
                            <div class='number'>ABC/XYZ</div>
                            <div class='caption'>Prioriza por inversión y previsibilidad.</div>
                        </div>
                        <div class='item'>
                            <div class='number'>ROP + SS</div>
                            <div class='caption'>Repón con criterio de ingeniería de inventarios.</div>
                        </div>
                        <div class='item'>
                            <div class='number'>14 días</div>
                            <div class='caption'>Prueba guiada para medir valor antes de suscribirte.</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
        )

        st.markdown(
                """
                <div class='of-grid'>
                    <div class='of-card'>
                        <strong>Detecta efectivo atrapado</strong>
                        <p>Identifica sobrestock, demanda muerta y referencias que hoy inmovilizan caja.</p>
                    </div>
                    <div class='of-card'>
                        <strong>Evita quiebres costosos</strong>
                        <p>Calcula stock de seguridad y punto de reorden por SKU con lead time real.</p>
                    </div>
                    <div class='of-card'>
                        <strong>Empieza sin integración compleja</strong>
                        <p>Usa plantillas listas en CSV/XLSX y conecta el ERP después como servicio premium.</p>
                    </div>
                    <div class='of-card'>
                        <strong>Habla el idioma industrial</strong>
                        <p>Incluye empaque mínimo, limpieza financiera y lógica para químicos y catalizadores.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
        )

        st.markdown("### Qué pasa en tu prueba")
        st.markdown(
                """
                <div class='of-steps'>
                    <div><strong>1.</strong> Descargas plantillas oficiales de Inventario, Ventas y Catálogo.</div>
                    <div><strong>2.</strong> Subes tus datos y el sistema corrige notas crédito, formatos y campos base.</div>
                    <div><strong>3.</strong> Ves capital inmovilizado, riesgo de quiebre, ROP y sugerencia de compra.</div>
                    <div><strong>4.</strong> Exportas resultados y validas si el ahorro y el control justifican la suscripción.</div>
                </div>
                """,
                unsafe_allow_html=True,
        )


def _render_plan_strip() -> None:
        cards: list[str] = []
        for key in ("starter", "pro", "enterprise"):
                plan = PLAN_CATALOG[key]
                features = "<br>".join(f"• {item}" for item in plan["features"])
                highlight = " highlight" if key == "pro" else ""
                cards.append(
                        f"""
                        <div class='of-plan{highlight}'>
                            <div class='of-pill'>{plan['name']}</div>
                            <div class='price'>${plan['price_monthly_usd']}<span style='font-size:.9rem; color:var(--muted)'>/mes</span></div>
                            <div class='of-mini-note'>{features}</div>
                        </div>
                        """
                )

        st.markdown("### Planes pensados para crecer contigo")
        st.markdown(f"<div class='of-plan-strip'>{''.join(cards)}</div>", unsafe_allow_html=True)


def _render_trust_and_faq() -> None:
        st.markdown("### Transparencia, seguridad y confianza")
        st.markdown(
                """
                <div class='of-trust-grid'>
                  <div class='of-trust-card'>
                        <strong>Tus datos no se venden ni se comparten.</strong>
                        <p class='of-mini-note'>Cada tenant opera con su propia cuenta y sus datos se usan únicamente para análisis internos de inventario.</p>
                  </div>
                  <div class='of-trust-card'>
                        <strong>Subes archivos para analizar, no para perder control.</strong>
                        <p class='of-mini-note'>El sistema valida columnas, limpia inconsistencias y conserva el foco en recomendaciones de compra y capital inmovilizado.</p>
                  </div>
                  <div class='of-trust-card'>
                        <strong>Modelo claro de servicio.</strong>
                        <p class='of-mini-note'>La suscripción cubre análisis y uso del SaaS. La integración ERP avanzada se cotiza por separado.</p>
                  </div>
                  <div class='of-trust-card'>
                        <strong>Prueba antes de comprometerte.</strong>
                        <p class='of-mini-note'>La prueba de 14 días está pensada para demostrar valor real con tus propios datos y sin fricción técnica inicial.</p>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
        )

        st.markdown("### Preguntas frecuentes")
        st.markdown(
                "<div class='of-faq-shell'><p class='of-mini-note'>"
                "Abre cada ventana para entender exactamente qué hace la app, cómo trata tus datos y cómo evoluciona a suscripción."
                "</p></div>",
                unsafe_allow_html=True,
        )

        faq_cols = st.columns(3)
        with faq_cols[0]:
                with st.popover("¿Qué hace la app exactamente?"):
                        st.write(
                                "OptiFerre SaaS analiza inventario y ventas para mostrar capital inmovilizado,"
                                " riesgo de quiebre, punto de reorden, stock de seguridad y sugerencia de compra."
                        )
                        st.write(
                                "El objetivo es ayudarte a comprar mejor, reducir sobrestock y evitar quedarte sin producto clave."
                        )
        with faq_cols[1]:
                with st.popover("¿Cómo se sube y procesa la información?"):
                        st.write(
                                "Descargas plantillas oficiales, subes tus archivos CSV o Excel y el sistema valida las columnas requeridas."
                        )
                        st.write(
                                "Luego normaliza fechas, cantidades y notas crédito para correr el motor analítico de forma consistente."
                        )
        with faq_cols[2]:
                with st.popover("¿Dónde se guarda la información?"):
                        st.write(
                                "La configuración de la cuenta y las suscripciones se guardan en base de datos."
                        )
                        st.write(
                                "Los archivos cargados se usan para generar el análisis del tenant actual dentro de la sesión de trabajo."
                        )

        faq_cols_2 = st.columns(3)
        with faq_cols_2[0]:
                with st.popover("¿Quién puede ver mis datos?"):
                        st.write(
                                "Tus datos no están pensados para ser visibles por otros clientes. La experiencia es multitenant y cada cuenta opera separada."
                        )
        with faq_cols_2[1]:
                with st.popover("¿Qué seguridad ofrece la app?"):
                        st.write(
                                "La app usa autenticación por usuario, despliegue en contenedor, configuración separada por entorno y base de datos dedicada."
                        )
                        st.write(
                                "Además, los secretos deben administrarse fuera del repositorio, por ejemplo en Coolify."
                        )
        with faq_cols_2[2]:
                with st.popover("¿Qué pasa después de la prueba?"):
                        st.write(
                                "Si el resultado te demuestra valor, activas un plan y mantienes acceso al análisis."
                        )
                        st.write(
                                "Si luego quieres integrar ERP, automatizar abastecimiento o ampliar branding, eso se maneja como evolución premium."
                        )


def render() -> None:
        left, right = st.columns([1.35, 0.95], gap="large")

        with left:
                _render_hero()
                _render_plan_strip()
                _render_trust_and_faq()

        with right:
                st.markdown(
                        """
                        <div class='of-form-shell'>
                            <div class='of-eyebrow'>Empieza hoy</div>
                            <h3 style='margin:8px 0'>Crea tu cuenta o entra a tu tenant</h3>
                            <p class='of-mini-note'>
                                La prueba incluye dashboard ejecutivo, análisis ABC/XYZ, stock de seguridad,
                                punto de reorden, sugerencia de compra y exportación de resultados.
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                )

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
                                email = st.text_input("Email corporativo", key="signup_email")
                                password = st.text_input("Contraseña segura (mín. 8)", type="password", key="signup_pwd")
                                accept = st.checkbox("Acepto los términos y la política de privacidad.")
                                submitted = st.form_submit_button("Activar mi prueba gratis", use_container_width=True)
                        if submitted:
                                if not all([company, full_name, email, password]) or len(password) < 8:
                                        st.error("Completa todos los campos. La contraseña debe tener al menos 8 caracteres.")
                                elif not accept:
                                        st.error("Debes aceptar los términos.")
                                else:
                                        try:
                                                register_tenant(company, email, password, full_name)
                                                data = authenticate(email, password)
                                                if data:
                                                        login(data)
                                                        st.success("Cuenta creada. ¡Tu prueba de 14 días ya está activa! 🎉")
                                                        st.rerun()
                                        except Exception as exc:  # pragma: no cover
                                                st.error(f"No fue posible crear la cuenta: {exc}")

                st.caption(
                        "Sin instalación local. Sin integración ERP obligatoria al inicio. "
                        "Empiezas con archivos y luego escalas a suscripción y automatización."
                )
