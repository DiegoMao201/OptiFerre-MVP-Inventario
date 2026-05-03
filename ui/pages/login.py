"""Página pública de acceso y conversión comercial."""
from __future__ import annotations

import base64
from pathlib import Path
from textwrap import dedent

import streamlit as st

from core.auth import (
        authenticate,
        create_password_reset_request,
        login,
        register_tenant,
        reset_password_with_token,
        validate_password_reset_token,
)
from core.billing import PLAN_CATALOG
from core.config import get_settings
from core.mail import (
        send_account_created_email,
        send_login_notice_email,
        send_password_changed_email,
        send_password_reset_email,
)
from core.support import create_support_ticket


ACTIONABLE_PILLARS = [
        {
                "title": "14 días gratis",
                "caption": "Pruébalo con tu propio Excel y mira tu plata atrapada.",
                "eyebrow": "Empieza sin pagar",
                "summary": "En 14 días subes tus archivos, ves dónde tienes plata muerta en bodega y decides si te sirve antes de soltar un peso.",
                "benefits": [
                        "Ves de una qué productos no se mueven y cuánto dinero te están comiendo.",
                        "Sirve para que tú o tu socio vean el problema con números claros, no con corazonadas.",
                        "No necesitas otro sistema: arrancas con el mismo Excel que ya manejas.",
                ],
                "cta": "Crea tu cuenta y mira tu inventario con otros ojos hoy mismo.",
        },
        {
                "title": "💰 Plata muerta",
                "caption": "Qué productos llevan meses quietos y cuánto te cuestan.",
                "eyebrow": "Lo que no rota",
                "summary": "Te decimos exactamente qué referencias están durmiendo en la bodega y cuánto dinero tienes congelado en ellas.",
                "benefits": [
                        "Sabes qué rematar, devolver al proveedor o dejar de pedir.",
                        "Dejas de comprar más de lo mismo que ya está muerto en bodega.",
                        "Liberas plata para invertirla en lo que sí se vende rápido.",
                ],
                "cta": "Entra y descubre qué productos te están comiendo el flujo de caja.",
        },
        {
                "title": "📦 Qué comprar",
                "caption": "Cuánto y cuándo pedir, sin quedarte sin stock.",
                "eyebrow": "Comprar con cabeza",
                "summary": "En vez de pedir 'a ojo', te damos un número claro de cuánto comprar de cada producto para no quebrarte y no sobrar.",
                "benefits": [
                        "Dejas de perder ventas porque no tenías el producto que el cliente pidió.",
                        "Dejas de meter plata en cosas que se van a quedar quietas 6 meses.",
                        "Le bajas presión a las compras de último minuto y a los pedidos urgentes.",
                ],
                "cta": "Activa tu cuenta y mira la lista de compra recomendada para tu negocio.",
        },
        {
                "title": "⚠️ Cuánto pierdes",
                "caption": "En pesos: cuánta plata tienes congelada cada mes.",
                "eyebrow": "Tu plata atrapada",
                "summary": "Te mostramos en pesos cuánto dinero está parado en bodega que podrías estar usando para comprar lo que sí se vende.",
                "benefits": [
                        "Entiendes cuánto te cuesta cada mes seguir comprando como hoy.",
                        "Tienes un número claro para hablar con tu socio, contador o banco.",
                        "Decides con cabeza fría qué hacer primero para recuperar caja.",
                ],
                "cta": "Empieza la prueba y mira tu negocio en plata, no en corazonadas.",
        },
]


def _build_logo_markup() -> str:
                logo_path = Path("logo_nexus.png")
                if not logo_path.exists():
                                return ""
                encoded = base64.b64encode(logo_path.read_bytes()).decode("ascii")
                return dedent(
                                f"""
                                <div class='of-logo-tech-shell'>
                                        <div class='of-logo-orbit orbit-a'></div>
                                        <div class='of-logo-orbit orbit-b'></div>
                                        <div class='of-logo-orbit orbit-c'></div>
                                        <div class='of-logo-scan'></div>
                                        <div class='of-logo-core-glow'></div>
                                        <img class='of-brand-logo' src='data:image/png;base64,{encoded}' alt='Nexus Pro'>
                                </div>
                                """
                ).strip()


def _render_top_stage() -> None:
                logo_col, title_col = st.columns([1, 1], gap="large")
                with logo_col:
                                st.markdown(
                                                                f"<div class='of-stage-logo-wrap'><div class='of-logo-panel'>{_build_logo_markup()}<div class='of-logo-caption'>Mira tu inventario en plata, no en corazonadas.</div></div></div>",

                with title_col:
                                st.markdown(
                                                dedent(
                                                                """
                                                                <div class="of-stage-title-wrap">
                                                                        <div class="of-eyebrow">OptiFerre · Para ferreterías y depósitos</div>
                                                                        <h1 class="of-stage-title of-shimmer-title">Tienes plata muerta en tu bodega y todavía no lo sabes.</h1>
                                                                        <p class="of-stage-lead">Sube tu Excel de inventario y de ventas. En minutos te decimos qué productos están quietos, cuáles se te van a acabar y cuánto deberías comprar la próxima vez. Sin instalar nada y sin tecnicismos.</p>
                                                                        <div class="of-chip-row">
                                                                                <span class="of-chip">💰 14 días gratis</span>
                                                                                <span class="of-chip">📄 Funciona con tu Excel</span>
                                                                                <span class="of-chip">🔧 Para ferreterías, materiales y depósitos</span>
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
                                                        <div class="of-eyebrow">Para ferreterías, depósitos, materiales y distribuidores</div>
                                                        <h2 class="of-shimmer-title">Deja de tener tu plata muerta en la bodega.</h2>
                                                        <p>
                                                                Subes tu archivo de inventario y de ventas. En minutos te mostramos qué productos llevan meses quietos,
                                                                cuáles se te van a acabar y cuánto deberías comprar de cada uno. Todo en pesos, en español claro,
                                                                y sin necesidad de cambiar de sistema.
                                                        </p>
                                                        <div class="of-proof-v2">
                                                                <div class="item">
                                                                        <div class="number">💰 Plata muerta</div>
                                                                        <div class="caption">Qué productos llevan meses sin moverse y cuánto te cuestan.</div>
                                                                </div>
                                                                <div class="item">
                                                                        <div class="number">📦 Compra justa</div>
                                                                        <div class="caption">Cuánto pedir de cada producto para no quebrarte y no sobrar.</div>
                                                                </div>
                                                                <div class="item">
                                                                        <div class="number">🆓 14 días</div>
                                                                        <div class="caption">Pruébalo con tu propio Excel antes de pagar un peso.</div>
                                                                </div>
                                                        </div>
                                                </div>
                                                """
                                ),
                                unsafe_allow_html=True,
                )


def _render_stats_bar() -> None:
                st.markdown("<div class='of-page-block'><div class='of-soft-panel'>", unsafe_allow_html=True)
                st.markdown(
                                "<p class='of-actionable-intro'>Toca cada bloque y mira cómo te ayuda a recuperar plata, vender más y comprar con cabeza.</p>",
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
                st.markdown("</div></div>", unsafe_allow_html=True)


def _render_feature_grid() -> None:
                st.markdown("### <span class='of-shimmer-title'>¿Por qué lo usan tantos ferreteros?</span>", unsafe_allow_html=True)
                st.markdown(
                                "<p class='of-mini-note' style='margin-bottom:18px'>Todo lo que necesitas para dejar de comprar a ojo y empezar a vender lo que sí rota.</p>",
                                unsafe_allow_html=True,
                )
                st.markdown(
                                dedent(
                                                """
                                                <div class="of-feature-grid-v2">
                                                        <div class="of-feature-card-v2 card-hover">
                                                                <div class="of-feature-icon">01</div>
                                                                <h4>Sube tu Excel y listo</h4>
                                                                <p>Carga el mismo archivo que ya manejas. No tienes que comprar otro programa ni cambiar tu sistema.</p>
                                                        </div>
                                                        <div class="of-feature-card-v2 card-hover">
                                                                <div class="of-feature-icon">02</div>
                                                                <h4>Funciona con tu negocio</h4>
                                                                <p>Ferretería, materiales, agro, distribuidor o tienda de barrio. Si vendes con stock, te sirve.</p>
                                                        </div>
                                                        <div class="of-feature-card-v2 card-hover">
                                                                <div class="of-feature-icon">03</div>
                                                                <h4>Tablero claro en pesos</h4>
                                                                <p>Ves de una cuánta plata tienes muerta, qué se va a acabar y por dónde empezar a sacar caja.</p>
                                                        </div>
                                                        <div class="of-feature-card-v2 card-hover">
                                                                <div class="of-feature-icon">04</div>
                                                                <h4>Simula sin riesgo</h4>
                                                                <p>Mira qué pasaría si bajas stock o cambias proveedor, antes de tocar la bodega real.</p>
                                                        </div>
                                                        <div class="of-feature-card-v2 card-hover">
                                                                <div class="of-feature-icon">05</div>
                                                                <h4>Demo de prueba</h4>
                                                                <p>Si todavía no quieres subir tu data, prueba con un negocio de ejemplo y mira cómo se ve.</p>
                                                        </div>
                                                        <div class="of-feature-card-v2 card-hover">
                                                                <div class="of-feature-icon">06</div>
                                                                <h4>Crece a tu ritmo</h4>
                                                                <p>Empiezas con archivos. Cuando ya veas la plata recuperada, decides si quieres conectar más cosas.</p>
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
                                                        <div class="of-eyebrow">Empieza ya · 14 días gratis</div>
                                                        <h3>Mira dónde tienes la plata atrapada</h3>
                                                        <p class="of-mini-note">Crea tu cuenta gratis y sube tu Excel. En minutos vas a ver qué productos están muertos, cuáles se te van a acabar y cuánto deberías comprar la próxima vez.</p>
                                                </div>
                                                """
                                ),
                                unsafe_allow_html=True,
                )


def _render_trust_and_proof() -> None:
                st.markdown("### <span class='of-shimmer-title'>Negocios como el tuyo tienen millones quietos sin saberlo</span>", unsafe_allow_html=True)
                st.markdown(
                                dedent(
                                                """
                                                <div class="of-proof-grid-v2">
                                                        <div class="of-proof-card-v2 testimonial-card">
                                                                <div class="of-eyebrow">Lo que te resuelve</div>
                                                                <p>"Pasas de un Excel desordenado a saber con números qué productos te están haciendo perder plata y cuáles te están haciendo perder ventas."</p>
                                                                <div class="of-proof-person">Hecho para el dueño, el comprador y el que maneja la caja.</div>
                                                        </div>
                                                        <div class="of-proof-card-v2 testimonial-card">
                                                                <div class="of-eyebrow">Tu información es tuya</div>
                                                                <p>"Tu Excel y tus ventas no se venden ni se comparten. Cada negocio trabaja en su propio espacio privado y nadie más lo ve."</p>
                                                                <div class="of-proof-person">Primero la confianza, después la plata.</div>
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

        st.markdown("### <span class='of-shimmer-title'>Planes claros, sin sorpresas en la factura</span>", unsafe_allow_html=True)
        st.markdown(
                "<p class='of-mini-note' style='margin-bottom:18px'>Empiezas gratis 14 días. Si te sirve, eliges plan. Si no, no pagas nada. Sin letra chiquita.</p>",
                unsafe_allow_html=True,
        )
        cols = st.columns(3)
        for col, card in zip(cols, cards):
                with col:
                        st.markdown(card, unsafe_allow_html=True)


def _render_faq() -> None:
                st.markdown("### <span class='of-shimmer-title'>Lo que más nos preguntan</span>", unsafe_allow_html=True)
                st.markdown(
                                "<div class='of-faq-shell'><p class='of-mini-note'>Lo que todo ferretero pregunta antes de probar la app. Abélo y mira la respuesta.</p></div>",
                                unsafe_allow_html=True,
                )

                faqs = [
                                (
                                                "¿Qué hace exactamente esta app?",
                                                [
                                                                "Toma tu inventario y tus ventas y te dice cuánta plata tienes muerta, qué productos te van a faltar y cuánto deberías comprar la próxima vez.",
                                                                "El objetivo es claro: que dejes de tener dinero quieto y que vendas más de lo que sí rota.",
                                                ],
                                ),
                                (
                                                "¿Es complicado subir mi Excel?",
                                                [
                                                                "No. Descargas la plantilla, pegas tu información o subes tu propio archivo y la app revisa que esté bien.",
                                                                "Si te falta una columna o una fecha, te avisa para arreglarlo en segundos.",
                                                ],
                                ),
                                (
                                                "¿Dónde queda guardada mi información?",
                                                [
                                                                "Tu cuenta y tus análisis quedan en una base de datos privada de tu empresa.",
                                                                "Solo se usan para mostrarte tus resultados. No los compartimos con nadie más.",
                                                ],
                                ),
                                (
                                                "¿Otra ferretería va a ver mi inventario?",
                                                [
                                                                "No. Cada negocio tiene su espacio aparte. Tu competencia no ve nada de lo tuyo.",
                                                ],
                                ),
                                (
                                                "¿Qué tan segura es la app?",
                                                [
                                                                "Entras con usuario y contraseña, los datos viajan encriptados y cada empresa tiene su propio espacio.",
                                                                "Nadie ve tus archivos sin que tú lo autorices.",
                                                ],
                                ),
                                (
                                                "¿Qué pasa cuando se acaba la prueba gratis?",
                                                [
                                                                "Si te sirvió, eliges plan y sigues viendo tu negocio claro mes a mes.",
                                                                "Si no te sirvió, no pagas nada y listo. Sin letra chiquita ni cobros sorpresa.",
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
                                                        <div class="of-eyebrow">Hoy mismo · Sin instalar nada</div>
                                                        <h3 class="of-shimmer-title">Hoy puedes saber cuánta plata tienes muerta en bodega.</h3>
                                                        <p class="of-mini-note">Subes tu Excel, miras los números y decides qué hacer. En 14 días gratis lo pruebas con tu propia data, sin tarjeta y sin compromiso.</p>
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
                                                        <div class="of-eyebrow">¿Quieres que te lo muestre yo mismo?</div>
                                                        <div class="of-contact-name">DIEGO MAURICIO GARCIA</div>
                                                        <div class="of-contact-meta">Creador de OptiFerre</div>
                                                        <p class="of-mini-note">Si quieres que te lo enseñe en una llamada o que te ayude a subir tu primer Excel, escríbeme directo. Te respondo personalmente.</p>
                                                        <a class="of-contact-link" href="mailto:diegomao.201@gmail.com">diegomao.201@gmail.com</a>
                                                </div>
                                                """
                                ),
                                unsafe_allow_html=True,
                )


def _render_public_support_form() -> None:
                st.markdown("### <span class='of-shimmer-title'>¿Necesitas ayuda antes de entrar?</span>", unsafe_allow_html=True)
                st.markdown(
                                "<p class='of-mini-note' style='margin-bottom:16px'>Déjanos tu mensaje y te respondemos por correo. No tienes que crear cuenta para escribirnos.</p>",
                                unsafe_allow_html=True,
                )
                with st.form("public_support_form", clear_on_submit=True):
                                cols = st.columns(2)
                                with cols[0]:
                                                requester_name = st.text_input("Tu nombre")
                                                requester_email = st.text_input("Tu correo")
                                with cols[1]:
                                                company_name = st.text_input("Nombre del negocio")
                                                subject = st.text_input("¿Sobre qué es?")
                                message = st.text_area("Cuéntanos qué necesitas", height=160)
                                submitted = st.form_submit_button("Enviar mensaje", use_container_width=True)

                if submitted:
                                if not all([requester_name.strip(), requester_email.strip(), subject.strip(), message.strip()]):
                                                st.error("Llena tu nombre, correo, asunto y mensaje para que podamos ayudarte.")
                                else:
                                                ticket = create_support_ticket(
                                                                requester_name=requester_name,
                                                                requester_email=requester_email,
                                                                company_name=company_name,
                                                                subject=subject,
                                                                message=message,
                                                                source="public_page",
                                                                category="support",
                                                )
                                                st.success(f"Listo, recibimos tu mensaje #{ticket['id']}. Te respondemos al correo que dejaste.")


def _get_reset_token() -> str:
                try:
                                return str(st.query_params.get("reset_token", "") or "")
                except Exception:
                                return st.experimental_get_query_params().get("reset_token", [""])[0]


def _clear_reset_token() -> None:
                try:
                                if "reset_token" in st.query_params:
                                                del st.query_params["reset_token"]
                except Exception:
                                st.experimental_set_query_params()


def render() -> None:
                settings = get_settings()
                reset_token = _get_reset_token().strip()
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
                                if reset_token:
                                                token_data = validate_password_reset_token(reset_token)
                                                st.markdown("### <span class='of-shimmer-title'>Recupera tu acceso</span>", unsafe_allow_html=True)
                                                if not token_data:
                                                                st.error("El enlace ya no sirve o expiró. Pide otro desde 'Olvidé mi contraseña'.")
                                                else:
                                                                st.caption(f"Cambiando la contraseña de {token_data['email']}")
                                                                with st.form("password_reset_form", clear_on_submit=True):
                                                                                new_password = st.text_input("Nueva contraseña", type="password")
                                                                                confirm_password = st.text_input("Confirma la nueva contraseña", type="password")
                                                                                submitted_reset = st.form_submit_button("Guardar nueva contraseña", use_container_width=True)
                                                                if submitted_reset:
                                                                                if len(new_password) < 8:
                                                                                                st.error("La contraseña debe tener al menos 8 caracteres.")
                                                                                elif new_password != confirm_password:
                                                                                                st.error("Las contraseñas no son iguales.")
                                                                                else:
                                                                                                result = reset_password_with_token(reset_token, new_password)
                                                                                                if not result:
                                                                                                                st.error("No pudimos cambiar la contraseña. Pide otro enlace.")
                                                                                                else:
                                                                                                                send_password_changed_email(result["email"], result["full_name"])
                                                                                                                _clear_reset_token()
                                                                                                                st.success("Listo, contraseña cambiada. Ya puedes entrar con la nueva clave.")
                                else:
                                                tabs = st.tabs(["Entrar", "Crear cuenta gratis", "Olvidé mi contraseña"])

                                                with tabs[0]:
                                                                with st.form("login_form", clear_on_submit=False):
                                                                                email = st.text_input("Tu correo", placeholder="tu@correo.com")
                                                                                password = st.text_input("Contraseña", type="password")
                                                                                submitted = st.form_submit_button("Entrar a mi cuenta", use_container_width=True)
                                                                if submitted:
                                                                                data = authenticate(email, password)
                                                                                if data:
                                                                                                login(data)
                                                                                                send_login_notice_email(data["email"], data["full_name"], data["company_name"])
                                                                                                st.success(f"¡Bienvenido, {data['full_name']}!")
                                                                                                st.rerun()
                                                                                else:
                                                                                                st.error("Correo o contraseña incorrectos.")

                                                with tabs[1]:
                                                                with st.form("signup_form", clear_on_submit=False):
                                                                                company = st.text_input("Nombre de tu negocio")
                                                                                full_name = st.text_input("Tu nombre")
                                                                                email = st.text_input("Tu correo", key="signup_email")
                                                                                password = st.text_input("Crea tu contraseña (mínimo 8 caracteres)", type="password", key="signup_pwd")
                                                                                accept = st.checkbox("Acepto términos y política de datos.")
                                                                                submitted = st.form_submit_button("🚀 Empezar mi prueba gratis de 14 días", use_container_width=True)
                                                                if submitted:
                                                                                if not all([company, full_name, email, password]) or len(password) < 8:
                                                                                                st.error("Llena todos los campos. La contraseña debe tener mínimo 8 caracteres.")
                                                                                elif not accept:
                                                                                                st.error("Tienes que aceptar los términos para continuar.")
                                                                                else:
                                                                                                try:
                                                                                                                register_tenant(company, email, password, full_name)
                                                                                                                data = authenticate(email, password)
                                                                                                                if data:
                                                                                                                                login(data)
                                                                                                                                send_account_created_email(data["email"], data["full_name"], data["company_name"])
                                                                                                                                st.success("¡Cuenta creada! Ya tienes 14 días gratis para ver tu inventario en plata.")
                                                                                                                                st.rerun()
                                                                                                except Exception as exc:  # pragma: no cover
                                                                                                                st.error(f"No pudimos crear la cuenta: {exc}")

                                                with tabs[2]:
                                                                with st.form("password_reset_request", clear_on_submit=True):
                                                                                recovery_email = st.text_input("Tu correo", placeholder="tu@correo.com")
                                                                                submitted_recovery = st.form_submit_button("Mandarme el enlace para recuperar", use_container_width=True)
                                                                if submitted_recovery:
                                                                                if not recovery_email.strip():
                                                                                                st.error("Escribe el correo con el que entras a tu cuenta.")
                                                                                else:
                                                                                                reset_data = create_password_reset_request(recovery_email)
                                                                                                if reset_data:
                                                                                                                reset_url = f"{settings.base_url}/?reset_token={reset_data['token']}"
                                                                                                                send_password_reset_email(reset_data["email"], reset_data["full_name"], reset_url)
                                                                                                st.success("Si tu correo está registrado, te mandamos un enlace para cambiar la contraseña.")

                                st.caption(
                                                "Sin instalar nada. Sin sistemas raros. Subes tu Excel y empiezas a ver tu plata."
                                )

                _render_trust_and_proof()
                _render_plan_strip()
                _render_faq()
                _render_final_cta()
                _render_contact_section()
                _render_public_support_form()
                st.markdown("</div>", unsafe_allow_html=True)
