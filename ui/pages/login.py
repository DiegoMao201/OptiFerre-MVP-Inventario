"""Página pública de acceso y conversión comercial."""
from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import streamlit as st

from core.auth import authenticate, login, register_tenant
from core.billing import PLAN_CATALOG


def _render_top_stage() -> None:
                logo_col, title_col = st.columns([0.9, 1.1], gap="large")
                with logo_col:
                                st.markdown("<div class='of-stage-logo-wrap'>", unsafe_allow_html=True)
                                logo_path = Path("logo_nexus.png")
                                if logo_path.exists():
                                                st.image(str(logo_path), width=210)
                                st.markdown("</div>", unsafe_allow_html=True)

                with title_col:
                                st.markdown(
                                                dedent(
                                                                """
                                                                <div class="of-stage-title-wrap">
                                                                        <div class="of-eyebrow">OptiFerre SaaS</div>
                                                                        <h1 class="of-stage-title">Diagnóstico ejecutivo de inventarios para empresas ferreteras e industriales</h1>
                                                                        <div class="of-chip-row">
                                                                                <span class="of-chip">Prueba gratuita de 14 días</span>
                                                                                <span class="of-chip">Sin integración ERP obligatoria</span>
                                                                        </div>
                                                                </div>
                                                                """
                                                ),
                                                unsafe_allow_html=True,
                                )


def _render_value_stage() -> None:
                st.markdown(
                                dedent(
                                                """
                                                <div class="of-hero-v2 card-hover">
                                                        <div class="of-eyebrow">Optimización B2B para ferretería e industria</div>
                                                        <h2>Reduce capital inmovilizado y repone con criterio técnico.</h2>
                                                        <p>
                                                                OptiFerre SaaS convierte archivos de inventario y ventas en una lectura ejecutiva de riesgo,
                                                                rotación y abastecimiento. En pocos minutos sabes dónde tienes dinero atrapado,
                                                                qué referencias están por quebrarse y cuánto deberías comprar realmente.
                                                        </p>
                                                        <div class="of-proof-v2">
                                                                <div class="item">
                                                                        <div class="number">ABC/XYZ</div>
                                                                        <div class="caption">Prioriza por inversión y previsibilidad.</div>
                                                                </div>
                                                                <div class="item">
                                                                        <div class="number">ROP + SS</div>
                                                                        <div class="caption">Repone con reglas de ingeniería y no por intuición.</div>
                                                                </div>
                                                                <div class="item">
                                                                        <div class="number">14 días</div>
                                                                        <div class="caption">Prueba guiada para validar valor antes de pagar.</div>
                                                                </div>
                                                        </div>
                                                </div>
                                                """
                                ),
                                unsafe_allow_html=True,
                )


def _render_stats_bar() -> None:
                st.markdown(
                                dedent(
                                                """
                                                <div class="of-stat-grid">
                                                        <div class="of-stat-card">
                                                                <div class="value">14 días</div>
                                                                <div class="caption">Prueba real para validar valor sin fricción técnica.</div>
                                                        </div>
                                                        <div class="of-stat-card">
                                                                <div class="value">ABC/XYZ</div>
                                                                <div class="caption">Clasificación para ordenar foco, caja y riesgo.</div>
                                                        </div>
                                                        <div class="of-stat-card">
                                                                <div class="value">ROP + SS</div>
                                                                <div class="caption">Reposición basada en demanda y lead time.</div>
                                                        </div>
                                                        <div class="of-stat-card">
                                                                <div class="value">ROI mensual</div>
                                                                <div class="caption">Costo de oportunidad sobre capital inmovilizado.</div>
                                                        </div>
                                                </div>
                                                """
                                ),
                                unsafe_allow_html=True,
                )


def _render_feature_grid() -> None:
                st.markdown("### ¿Por qué OptiFerre?")
                st.markdown(
                                "<p class='of-mini-note' style='margin-bottom:18px'>Todo lo necesario para pasar de archivos desordenados a decisiones concretas de abastecimiento.</p>",
                                unsafe_allow_html=True,
                )
                st.markdown(
                                dedent(
                                                """
                                                <div class="of-feature-grid-v2">
                                                        <div class="of-feature-card-v2 card-hover">
                                                                <div class="of-feature-icon">01</div>
                                                                <h4>Smart Importer</h4>
                                                                <p>Reconoce aliases comunes de ERP y reduce fricción de carga desde el primer intento.</p>
                                                        </div>
                                                        <div class="of-feature-card-v2 card-hover">
                                                                <div class="of-feature-icon">02</div>
                                                                <h4>Motor industrial</h4>
                                                                <p>Incluye guardarraíles para empaques mínimos, químicos y referencias sensibles.</p>
                                                        </div>
                                                        <div class="of-feature-card-v2 card-hover">
                                                                <div class="of-feature-icon">03</div>
                                                                <h4>Dashboard ejecutivo</h4>
                                                                <p>Muestra health score, tareas prioritarias, caja atrapada y presión sobre SKUs clase A.</p>
                                                        </div>
                                                        <div class="of-feature-card-v2 card-hover">
                                                                <div class="of-feature-icon">04</div>
                                                                <h4>Simulación operativa</h4>
                                                                <p>Compara escenarios de nivel de servicio para evitar sobrecomprar por reflejo.</p>
                                                        </div>
                                                        <div class="of-feature-card-v2 card-hover">
                                                                <div class="of-feature-icon">05</div>
                                                                <h4>Demo Mode</h4>
                                                                <p>Demuestra valor comercial sin esperar la data real del cliente en la primera reunión.</p>
                                                        </div>
                                                        <div class="of-feature-card-v2 card-hover">
                                                                <div class="of-feature-icon">06</div>
                                                                <h4>Modelo SaaS claro</h4>
                                                                <p>Suscripción para el SaaS e integraciones avanzadas como servicio premium separado.</p>
                                                        </div>
                                                </div>
                                                """
                                ),
                                unsafe_allow_html=True,
                )


def _render_form_shell() -> None:
                st.markdown(
                                dedent(
                                                """
                                                <div class="of-auth-card card-hover">
                                                        <div class="of-eyebrow">Empieza hoy</div>
                                                        <h3>Crea tu cuenta o entra a tu tenant</h3>
                                                        <p class="of-mini-note">La prueba incluye dashboard ejecutivo, clasificación ABC/XYZ, stock de seguridad, punto de reorden y exportación de resultados.</p>
                                                </div>
                                                """
                                ),
                                unsafe_allow_html=True,
                )


def _render_trust_and_proof() -> None:
                st.markdown("### Confianza y claridad")
                st.markdown(
                                dedent(
                                                """
                                                <div class="of-proof-grid-v2">
                                                        <div class="of-proof-card-v2 testimonial-card">
                                                                <div class="of-eyebrow">Qué resuelve</div>
                                                                <p>"Pasas de hojas dispersas a una lectura accionable de quiebres, sobrestock, ROP y compra sugerida."</p>
                                                                <div class="of-proof-person">Pensado para gerencia comercial, compras y operaciones.</div>
                                                        </div>
                                                        <div class="of-proof-card-v2 testimonial-card">
                                                                <div class="of-eyebrow">Cómo tratamos tu información</div>
                                                                <p>"Tus datos no se venden ni se comparten. Cada empresa opera como tenant separado y el análisis se usa para su propia toma de decisiones."</p>
                                                                <div class="of-proof-person">Transparencia primero, venta después.</div>
                                                        </div>
                                                </div>
                                                """
                                ),
                                unsafe_allow_html=True,
                )


def _render_plan_strip() -> None:
        cards: list[str] = []
        for key in ("starter", "pro", "enterprise"):
                plan = PLAN_CATALOG[key]
                highlight = " of-price-popular" if key == "pro" else ""
                badge = "<span class='of-popular-badge'>Más popular</span>" if key == "pro" else ""
                features = "".join(f"<li>{item}</li>" for item in plan["features"])
                cards.append(
                        dedent(
                                f"""
                                <div class="of-price-card{highlight} card-hover">
                                  {badge}
                                  <div class="of-pill">{plan['name']}</div>
                                  <div class="of-price-main">${plan['price_monthly_usd']}<span>/mes</span></div>
                                  <ul class="of-price-list">{features}</ul>
                                </div>
                                """
                        ).strip()
                )

        st.markdown("### Planes claros, sin letra pequeña")
        st.markdown(
                "<p class='of-mini-note' style='margin-bottom:18px'>Empieza con trial, comprueba valor y escala a servicios avanzados solo cuando tenga sentido.</p>",
                unsafe_allow_html=True,
        )
        cols = st.columns(3)
        for col, card in zip(cols, cards):
                with col:
                        st.markdown(card, unsafe_allow_html=True)


def _render_faq() -> None:
                st.markdown("### Preguntas frecuentes")
                st.markdown(
                                "<div class='of-faq-shell'><p class='of-mini-note'>Abre cada respuesta y entiende qué hace la app, cómo procesa la información y cómo evolucionas a suscripción sin sorpresas.</p></div>",
                                unsafe_allow_html=True,
                )

                faqs = [
                                (
                                                "¿Qué hace la app exactamente?",
                                                [
                                                                "Analiza inventario y ventas para mostrar capital inmovilizado, quiebres, punto de reorden, stock de seguridad y sugerencia de compra.",
                                                                "Su objetivo es ayudarte a comprar mejor, reducir sobrestock y proteger disponibilidad de referencias clave.",
                                                ],
                                ),
                                (
                                                "¿Cómo se sube y procesa la información?",
                                                [
                                                                "Descargas plantillas oficiales, subes CSV o Excel y el sistema valida las columnas requeridas.",
                                                                "Luego normaliza fechas, cantidades, notas crédito y estructura base para correr el análisis con consistencia.",
                                                ],
                                ),
                                (
                                                "¿Dónde se guarda la información?",
                                                [
                                                                "La cuenta, configuración y suscripción viven en base de datos.",
                                                                "Los archivos cargados se usan para construir el análisis del tenant actual dentro del flujo de trabajo de la aplicación.",
                                                ],
                                ),
                                (
                                                "¿Quién puede ver mis datos?",
                                                [
                                                                "El modelo es multitenant y cada empresa opera separada. No está pensada para compartir datos entre clientes.",
                                                ],
                                ),
                                (
                                                "¿Qué seguridad ofrece la app?",
                                                [
                                                                "Usa autenticación por usuario, despliegue en contenedor, variables separadas por entorno y una base de datos dedicada.",
                                                                "Los secretos se administran fuera del repositorio, por ejemplo en Coolify.",
                                                ],
                                ),
                                (
                                                "¿Qué pasa después de la prueba?",
                                                [
                                                                "Si el resultado te demuestra valor, activas un plan y mantienes acceso al análisis y al dashboard.",
                                                                "Si luego quieres integrar ERP, automatizar abastecimiento o ampliar el alcance, eso se gestiona como evolución premium.",
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


def _render_final_cta() -> None:
                st.markdown(
                                dedent(
                                                """
                                                <div class="of-final-cta">
                                                        <div class="of-eyebrow">OptiFerre SaaS</div>
                                                        <h3>Empieza con archivos. Escala a plataforma.</h3>
                                                        <p class="of-mini-note">Primero validas valor con la prueba y el dashboard. Luego decides si activas suscripción, integración ERP o automatización avanzada.</p>
                                                </div>
                                                """
                                ),
                                unsafe_allow_html=True,
                )


def render() -> None:
                st.markdown(
                                "<div class='of-landing-canvas'><div class='of-glow orb-a'></div><div class='of-glow orb-b'></div><div class='of-glow orb-c'></div>",
                                unsafe_allow_html=True,
                )

                _render_top_stage()
                _render_stats_bar()

                hero_col, form_col = st.columns([1.55, 0.9], gap="large")

                with hero_col:
                                _render_value_stage()
                                _render_feature_grid()

                with form_col:
                                _render_form_shell()
                                tabs = st.tabs(["Iniciar sesión", "Crear cuenta"])

                                with tabs[0]:
                                                with st.form("login_form", clear_on_submit=False):
                                                                email = st.text_input("Email corporativo", placeholder="tu@empresa.com")
                                                                password = st.text_input("Contraseña", type="password")
                                                                submitted = st.form_submit_button("Entrar", use_container_width=True)
                                                if submitted:
                                                                data = authenticate(email, password)
                                                                if data:
                                                                                login(data)
                                                                                st.success(f"Bienvenido, {data['full_name']}")
                                                                                st.rerun()
                                                                else:
                                                                                st.error("Credenciales inválidas.")

                                with tabs[1]:
                                                with st.form("signup_form", clear_on_submit=False):
                                                                company = st.text_input("Nombre de la empresa")
                                                                full_name = st.text_input("Tu nombre completo")
                                                                email = st.text_input("Email corporativo", key="signup_email")
                                                                password = st.text_input("Contraseña segura (min. 8)", type="password", key="signup_pwd")
                                                                accept = st.checkbox("Acepto términos, política de privacidad y tratamiento de datos.")
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
                                                                                                                st.success("Cuenta creada. Tu prueba de 14 días ya está activa.")
                                                                                                                st.rerun()
                                                                                except Exception as exc:  # pragma: no cover
                                                                                                st.error(f"No fue posible crear la cuenta: {exc}")

                                st.caption(
                                                "Sin instalación local. Sin integración ERP obligatoria al inicio. Empiezas con archivos y escalas cuando el valor esté comprobado."
                                )

                _render_trust_and_proof()
                _render_plan_strip()
                _render_faq()
                _render_final_cta()
                st.markdown("</div>", unsafe_allow_html=True)
