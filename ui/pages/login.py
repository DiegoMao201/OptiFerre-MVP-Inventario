"""Página pública de acceso y conversión comercial."""
from __future__ import annotations

import base64
from pathlib import Path
from textwrap import dedent

import streamlit as st

from core.auth import authenticate, login, register_tenant
from core.billing import PLAN_CATALOG


ACTIONABLE_PILLARS = [
        {
                "title": "14 días",
                "caption": "Prueba real para validar valor sin fricción técnica.",
                "eyebrow": "Prueba guiada",
                "summary": "Activas una prueba de 14 días para cargar archivos, revisar el diagnóstico y entender el retorno antes de pagar.",
                "benefits": [
                        "Te deja ver rápidamente caja atrapada, quiebres y sugerencias de compra.",
                        "Sirve para demostrar valor interno antes de comprometer presupuesto.",
                        "Empiezas con archivos sin depender de una integración compleja desde el día uno.",
                ],
                "cta": "Crea tu cuenta para activar la prueba y ver beneficios reales con tus datos o con la demo guiada.",
        },
        {
                "title": "ABC/XYZ",
                "caption": "Clasificación para ordenar foco, caja y riesgo.",
                "eyebrow": "Prioridad operativa",
                "summary": "ABC/XYZ te ayuda a separar lo más importante por valor e identificar qué referencias tienen demanda más estable o más impredecible.",
                "benefits": [
                        "Te enfoca en los productos que más afectan caja y disponibilidad.",
                        "Facilita reuniones más claras entre compras, finanzas y operaciones.",
                        "Permite definir políticas distintas según criticidad y variabilidad.",
                ],
                "cta": "Ingresa para ver cómo la clasificación aterriza decisiones concretas en tu inventario.",
        },
        {
                "title": "ROP + SS",
                "caption": "Reposición basada en demanda y lead time.",
                "eyebrow": "Compra con criterio",
                "summary": "ROP y stock de seguridad convierten la intuición en una regla clara de reposición para reducir quiebres y evitar compras infladas.",
                "benefits": [
                        "Da una referencia concreta de cuándo comprar y cuánto proteger.",
                        "Reduce la dependencia de decisiones urgentes de último minuto.",
                        "Mejora equilibrio entre nivel de servicio y capital inmovilizado.",
                ],
                "cta": "Activa tu acceso para ver la sugerencia calculada con tus propias referencias y movimientos.",
        },
        {
                "title": "ROI mensual",
                "caption": "Costo de oportunidad sobre capital inmovilizado.",
                "eyebrow": "Impacto financiero",
                "summary": "Este indicador muestra cuánto dinero podrías liberar o dejar de castigar cada mes si corriges sobrestock, rotación y abastecimiento.",
                "benefits": [
                        "Aterriza el problema de inventario en lenguaje financiero y gerencial.",
                        "Ayuda a priorizar acciones por impacto económico, no solo por percepción.",
                        "Sirve para justificar decisiones frente a dirección o socios.",
                ],
                "cta": "Entra a la prueba para convertir el problema operativo en una conversación clara de retorno y caja.",
        },
]


def _build_logo_markup() -> str:
                logo_path = Path("logo_nexus.png")
                if not logo_path.exists():
                                return ""
                encoded = base64.b64encode(logo_path.read_bytes()).decode("ascii")
                return f"<img class='of-brand-logo' src='data:image/png;base64,{encoded}' alt='Nexus Pro'>"


def _render_top_stage() -> None:
                logo_col, title_col = st.columns([1, 1], gap="large")
                with logo_col:
                                st.markdown(
                                                f"<div class='of-stage-logo-wrap'><div class='of-logo-panel'>{_build_logo_markup()}<div class='of-logo-caption'>Analítica de inventarios con visibilidad clara, contraste limpio y presencia comercial.</div></div></div>",
                                                unsafe_allow_html=True,
                                )

                with title_col:
                                st.markdown(
                                                dedent(
                                                                """
                                                                <div class="of-stage-title-wrap">
                                                                        <div class="of-eyebrow">OptiFerre</div>
                                                                        <h1 class="of-stage-title">Diagnóstico <span class="of-shimmer-text">ejecutivo</span> de inventarios para empresas que gestionan stock</h1>
                                                                        <p class="of-stage-lead">Sube inventario y movimientos, obtén lectura ejecutiva de caja atrapada, riesgo de quiebre y compra sugerida con una experiencia más clara, visible y tecnológica.</p>
                                                                        <div class="of-chip-row">
                                                                                <span class="of-chip">14 días gratis</span>
                                                                                <span class="of-chip">Cero integración ERP</span>
                                                                                <span class="of-chip">Cualquier tipo de inventario</span>
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
                                                        <div class="of-eyebrow">Optimización B2B para cualquier operación con inventario</div>
                                                        <h2>Reduce capital inmovilizado y repone con <span class="of-shimmer-text">criterio</span>.</h2>
                                                        <p>
                                                                OptiFerre convierte archivos de inventario y movimientos en una lectura ejecutiva de riesgo,
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
                                "<p class='of-actionable-intro'>Haz clic en cada bloque para entender qué resuelve, cómo se aplica y por qué conviene iniciar la prueba.</p>",
                                unsafe_allow_html=True,
                )
                cols = st.columns(4)
                for col, item in zip(cols, ACTIONABLE_PILLARS):
                                with col:
                                                with st.popover(item["title"], use_container_width=True):
                                                                st.markdown(
                                                                                dedent(
                                                                                                f"""
                                                                                                <div class="of-stat-popover-kicker">{item['eyebrow']}</div>
                                                                                                <div class="of-stat-popover-title">{item['title']}</div>
                                                                                                <p class="of-mini-note" style="margin-top:8px; margin-bottom:10px; color:#102C49;">{item['summary']}</p>
                                                                                                """
                                                                                ),
                                                                                unsafe_allow_html=True,
                                                                )
                                                                for benefit in item["benefits"]:
                                                                                st.write(f"- {benefit}")
                                                                st.info(item["cta"])
                                                st.markdown(
                                                                f"<div class='of-stat-caption-card'>{item['caption']}</div>",
                                                                unsafe_allow_html=True,
                                                )


def _render_feature_grid() -> None:
                st.markdown("### ¿Por qué <span class='of-shimmer-text'>OptiFerre</span>?", unsafe_allow_html=True)
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
                                                                <h4>Motor adaptable</h4>
                                                                <p>Se ajusta a distintos tipos de inventario, políticas de compra y estructuras de catálogo.</p>
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
                                                                <h4>Demo guiada</h4>
                                                                <p>Demuestra valor comercial sin esperar la data real del cliente en la primera reunión.</p>
                                                        </div>
                                                        <div class="of-feature-card-v2 card-hover">
                                                                <div class="of-feature-icon">06</div>
                                                                <h4>Crecimiento por etapas</h4>
                                                                <p>Empiezas con una prueba guiada y luego sumas automatizaciones o integraciones solo cuando ya ves valor real.</p>
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
                                                        <h3>Crea tu cuenta o entra a tu espacio</h3>
                                                        <p class="of-mini-note">La prueba incluye dashboard ejecutivo, clasificación ABC/XYZ, stock de seguridad, punto de reorden y exportación de resultados con lectura clara en cada campo.</p>
                                                </div>
                                                """
                                ),
                                unsafe_allow_html=True,
                )


def _render_trust_and_proof() -> None:
                st.markdown("### Confianza y <span class='of-shimmer-text'>claridad</span>", unsafe_allow_html=True)
                st.markdown(
                                dedent(
                                                """
                                                <div class="of-proof-grid-v2">
                                                        <div class="of-proof-card-v2 testimonial-card">
                                                                <div class="of-eyebrow">Qué resuelve</div>
                                                                <p>"Pasas de hojas dispersas a una lectura accionable de quiebres, sobrestock, ROP y compra sugerida."</p>
                                                                <div class="of-proof-person">Pensado para equipos de compras, operaciones, finanzas y gerencia.</div>
                                                        </div>
                                                        <div class="of-proof-card-v2 testimonial-card">
                                                                <div class="of-eyebrow">Cómo tratamos tu información</div>
                                                                <p>"Tus datos no se venden ni se comparten. Cada empresa trabaja en un espacio privado y el análisis se usa solo para su propia toma de decisiones."</p>
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
                                                                                                                                <div class="of-price-card{highlight} card-hover" tabindex="0">
                                  {badge}
                                  <div class="of-pill">{plan['name']}</div>
                                  <div class="of-price-main">${plan['price_monthly_usd']}<span>/mes</span></div>
                                  <ul class="of-price-list">{features}</ul>
                                </div>
                                """
                        ).strip()
                )

        st.markdown("### Planes <span class='of-shimmer-text'>claros</span>, sin letra pequeña", unsafe_allow_html=True)
        st.markdown(
                "<p class='of-mini-note' style='margin-bottom:18px'>Empieza con trial, comprueba valor y escala a servicios avanzados solo cuando tenga sentido.</p>",
                unsafe_allow_html=True,
        )
        cols = st.columns(3)
        for col, card in zip(cols, cards):
                with col:
                        st.markdown(card, unsafe_allow_html=True)


def _render_faq() -> None:
                st.markdown("### Preguntas <span class='of-shimmer-text'>frecuentes</span>", unsafe_allow_html=True)
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
                                                                "Los archivos cargados se usan para construir el análisis de tu empresa dentro del flujo de trabajo de la aplicación.",
                                                ],
                                ),
                                (
                                                "¿Quién puede ver mis datos?",
                                                [
                                                                "Cada empresa tiene su espacio separado. La app no comparte información entre clientes.",
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
                                                        <div class="of-eyebrow">OptiFerre</div>
                                                        <h3>Empieza con <span class="of-shimmer-text">archivos</span>. Escala a plataforma.</h3>
                                                        <p class="of-mini-note">Primero validas valor con la prueba y el dashboard. Luego decides si activas suscripción, integración ERP o automatización avanzada.</p>
                                                </div>
                                                """
                                ),
                                unsafe_allow_html=True,
                )


def _render_contact_section() -> None:
                st.markdown(
                                dedent(
                                                """
                                                <div class="of-contact-panel">
                                                        <div class="of-eyebrow">Contacto directo</div>
                                                        <div class="of-contact-name">DIEGO MAURICIO GARCIA</div>
                                                        <div class="of-contact-meta">Arquitecto y desarrollador de OptiFerre</div>
                                                        <p class="of-mini-note">Si quieres revisar integración, despliegue, demo guiada, automatización o una implementación más potente, este es el punto de contacto directo.</p>
                                                        <a class="of-contact-link" href="mailto:diegomao.201@gmail.com">diegomao.201@gmail.com</a>
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
                _render_contact_section()
                st.markdown("</div>", unsafe_allow_html=True)
