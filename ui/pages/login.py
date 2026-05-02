"""Página pública de acceso y conversión comercial."""
from __future__ import annotations

from textwrap import dedent
from pathlib import Path

import streamlit as st

from core.auth import authenticate, login, register_tenant
from core.billing import PLAN_CATALOG


def _render_hero() -> None:
        st.markdown(
                dedent(
                        """
                        <div class="of-hero">
                          <div class="of-eyebrow">Optimizacion B2B para ferreteria e industria</div>
                          <h1>Reduce capital inmovilizado y repone con criterio tecnico.</h1>
                          <p>
                                OptiFerre SaaS convierte archivos de inventario y ventas en una lectura ejecutiva de riesgo,
                                rotacion y abastecimiento. En pocos minutos sabes donde tienes dinero atrapado,
                                que referencias estan por quebrarse y cuanto deberias comprar realmente.
                          </p>
                          <div class="of-proof">
                                <div class="item">
                                  <div class="number">ABC/XYZ</div>
                                  <div class="caption">Prioriza por inversion y previsibilidad.</div>
                                </div>
                                <div class="item">
                                  <div class="number">ROP + SS</div>
                                  <div class="caption">Repone con reglas de ingenieria y no por intuicion.</div>
                                </div>
                                <div class="item">
                                  <div class="number">14 dias</div>
                                  <div class="caption">Prueba guiada para validar valor antes de pagar.</div>
                                </div>
                          </div>
                        </div>
                        """
                ),
                unsafe_allow_html=True,
        )

        st.markdown(
                dedent(
                        """
                        <div class="of-grid">
                          <div class="of-card">
                                <strong>Detecta efectivo atrapado</strong>
                                <p>Ubica sobrestock, inventario inmovilizado y referencias con baja salida que drenan caja.</p>
                          </div>
                          <div class="of-card">
                                <strong>Evita quiebres costosos</strong>
                                <p>Calcula stock de seguridad y punto de reorden por SKU usando demanda y lead time.</p>
                          </div>
                          <div class="of-card">
                                <strong>Empieza sin integracion compleja</strong>
                                <p>Sube CSV o Excel con plantillas oficiales y conecta el ERP despues si el negocio lo requiere.</p>
                          </div>
                          <div class="of-card">
                                <strong>Habla el idioma industrial</strong>
                                <p>Incluye empaques minimos, limpieza financiera y reglas especificas para quimicos.</p>
                          </div>
                        </div>
                        """
                ),
                unsafe_allow_html=True,
        )

        st.markdown("### Asi funciona la prueba")
        st.markdown(
                dedent(
                        """
                        <div class="of-steps">
                          <div><strong>1.</strong> Descargas plantillas y subes tu inventario y ventas.</div>
                          <div><strong>2.</strong> El sistema valida columnas, normaliza datos y corrige notas credito.</div>
                          <div><strong>3.</strong> Recibes dashboard ejecutivo, ABC/XYZ, ROP, stock de seguridad y sugerencia de compra.</div>
                          <div><strong>4.</strong> Evalua el ROI del analisis y activa la suscripcion si el valor es claro para tu operacion.</div>
                        </div>
                        """
                ),
                unsafe_allow_html=True,
        )


def _render_plan_strip() -> None:
        cards: list[str] = []
        for key in ("starter", "pro", "enterprise"):
                plan = PLAN_CATALOG[key]
                features = "<br>".join(f"• {item}" for item in plan["features"])
                highlight = " highlight" if key == "pro" else ""
                cards.append(
                        dedent(
                                f"""
                                <div class="of-plan{highlight}">
                                  <div class="of-pill">{plan['name']}</div>
                                  <div class="price">${plan['price_monthly_usd']}<span style="font-size:.9rem; color:var(--muted)">/mes</span></div>
                                  <div class="of-mini-note">{features}</div>
                                </div>
                                """
                        )
                )

        st.markdown("### Capacidad del producto")
        st.markdown(f"<div class='of-plan-strip'>{''.join(cards)}</div>", unsafe_allow_html=True)


def _render_trust_and_faq() -> None:
        st.markdown("### Transparencia, seguridad y confianza")
        st.markdown(
                dedent(
                        """
                        <div class="of-trust-grid">
                          <div class="of-trust-card">
                                <strong>Tus datos no se venden ni se comparten.</strong>
                                <p class="of-mini-note">Cada tenant trabaja sobre su propia cuenta y la informacion se usa para su analisis interno.</p>
                          </div>
                          <div class="of-trust-card">
                                <strong>Subes archivos para analizar, no para perder control.</strong>
                                <p class="of-mini-note">El sistema valida columnas, limpia inconsistencias y concentra el resultado en decisiones de compra.</p>
                          </div>
                          <div class="of-trust-card">
                                <strong>Modelo de servicio claro.</strong>
                                <p class="of-mini-note">La suscripcion cubre el SaaS. Integraciones ERP avanzadas y automatizaciones se cotizan aparte.</p>
                          </div>
                          <div class="of-trust-card">
                                <strong>Prueba antes de comprometerte.</strong>
                                <p class="of-mini-note">La prueba de 14 dias sirve para comprobar valor real con tus propios datos.</p>
                          </div>
                        </div>
                        """
                ),
                unsafe_allow_html=True,
        )

        st.markdown("### Preguntas frecuentes")
        st.markdown(
                "<div class='of-faq-shell'><p class='of-mini-note'>Abre cada respuesta y entiende como funciona la app, como trata tus datos y como evolucionas a suscripcion sin sorpresas.</p></div>",
                unsafe_allow_html=True,
        )

        faqs = [
                (
                        "¿Que hace la app exactamente?",
                        [
                                "Analiza inventario y ventas para mostrar capital inmovilizado, quiebres, punto de reorden, stock de seguridad y sugerencia de compra.",
                                "Su objetivo es ayudarte a comprar mejor, reducir sobrestock y proteger disponibilidad de referencias clave.",
                        ],
                ),
                (
                        "¿Como se sube y procesa la informacion?",
                        [
                                "Descargas plantillas oficiales, subes CSV o Excel y el sistema valida las columnas requeridas.",
                                "Luego normaliza fechas, cantidades, notas credito y estructura base para correr el analisis con consistencia.",
                        ],
                ),
                (
                        "¿Donde se guarda la informacion?",
                        [
                                "La cuenta, configuracion y suscripcion viven en base de datos.",
                                "Los archivos cargados se usan para construir el analisis del tenant actual dentro del flujo de trabajo de la aplicacion.",
                        ],
                ),
                (
                        "¿Quien puede ver mis datos?",
                        [
                                "El modelo es multitenant y cada empresa opera separada. No esta pensada para compartir datos entre clientes.",
                        ],
                ),
                (
                        "¿Que seguridad ofrece la app?",
                        [
                                "Usa autenticacion por usuario, despliegue en contenedor, variables separadas por entorno y una base de datos dedicada.",
                                "Los secretos se administran fuera del repositorio, por ejemplo en Coolify.",
                        ],
                ),
                (
                        "¿Que pasa despues de la prueba?",
                        [
                                "Si el resultado te demuestra valor, activas un plan y mantienes acceso al analisis y al dashboard.",
                                "Si luego quieres integrar ERP, automatizar abastecimiento o ampliar el alcance, eso se gestiona como evolucion premium.",
                        ],
                ),
        ]

        for row_start in range(0, len(faqs), 3):
                cols = st.columns(3)
                for col, (question, answers) in zip(cols, faqs[row_start: row_start + 3]):
                        with col:
                                with st.popover(question, use_container_width=True):
                                        for answer in answers:
                                                st.write(answer)


def render() -> None:
        top_left, top_right = st.columns([1.2, 1], gap="large")
        with top_left:
                logo_path = Path("logo_nexus.png")
                if logo_path.exists():
                        st.image(str(logo_path), width=190)
        with top_right:
                st.markdown(
                        dedent(
                                """
                                <div class="of-public-shell">
                                  <div class="of-public-topbar">
                                        <div>
                                          <div class="of-eyebrow">OptiFerre SaaS</div>
                                          <h2 style="margin:6px 0 0 0">Diagnostico ejecutivo de inventarios para empresas ferreteras e industriales</h2>
                                        </div>
                                        <div class="of-public-badge">Prueba gratuita de 14 dias</div>
                                  </div>
                                </div>
                                """
                        ),
                        unsafe_allow_html=True,
                )

        hero_col, form_col = st.columns([1.5, 0.9], gap="large")

        with hero_col:
                _render_hero()

        with form_col:
                st.markdown(
                        dedent(
                                """
                                <div class="of-form-shell">
                                  <div class="of-eyebrow">Empieza hoy</div>
                                  <h3 style="margin:8px 0">Crea tu cuenta o entra a tu tenant</h3>
                                  <p class="of-mini-note">La prueba incluye dashboard ejecutivo, clasificacion ABC/XYZ, stock de seguridad, punto de reorden y exportacion de resultados.</p>
                                </div>
                                """
                        ),
                        unsafe_allow_html=True,
                )

                tabs = st.tabs(["Iniciar sesion", "Crear cuenta"])

                with tabs[0]:
                        with st.form("login_form", clear_on_submit=False):
                                email = st.text_input("Email corporativo", placeholder="tu@empresa.com")
                                password = st.text_input("Contrasena", type="password")
                                submitted = st.form_submit_button("Entrar", use_container_width=True)
                        if submitted:
                                data = authenticate(email, password)
                                if data:
                                        login(data)
                                        st.success(f"Bienvenido, {data['full_name']}")
                                        st.rerun()
                                else:
                                        st.error("Credenciales invalidas.")

                with tabs[1]:
                        with st.form("signup_form", clear_on_submit=False):
                                company = st.text_input("Nombre de la empresa")
                                full_name = st.text_input("Tu nombre completo")
                                email = st.text_input("Email corporativo", key="signup_email")
                                password = st.text_input("Contrasena segura (min. 8)", type="password", key="signup_pwd")
                                accept = st.checkbox("Acepto terminos, politica de privacidad y tratamiento de datos.")
                                submitted = st.form_submit_button("Activar mi prueba gratis", use_container_width=True)
                        if submitted:
                                if not all([company, full_name, email, password]) or len(password) < 8:
                                        st.error("Completa todos los campos. La contrasena debe tener al menos 8 caracteres.")
                                elif not accept:
                                        st.error("Debes aceptar los terminos.")
                                else:
                                        try:
                                                register_tenant(company, email, password, full_name)
                                                data = authenticate(email, password)
                                                if data:
                                                        login(data)
                                                        st.success("Cuenta creada. Tu prueba de 14 dias ya esta activa.")
                                                        st.rerun()
                                        except Exception as exc:  # pragma: no cover
                                                st.error(f"No fue posible crear la cuenta: {exc}")

                st.caption(
                        "Sin instalacion local. Sin integracion ERP obligatoria al inicio. Empiezas con archivos y escalas cuando el valor este comprobado."
                )

        _render_plan_strip()
        _render_trust_and_faq()
