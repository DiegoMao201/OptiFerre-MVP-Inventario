"""Página privada de soporte y tickets para clientes autenticados."""
from __future__ import annotations

import streamlit as st

from core.auth import require_login
from core.config import get_settings
from core.support import (
    add_ticket_message,
    create_support_ticket,
    list_support_tickets,
    list_ticket_messages,
    update_ticket_status,
)


def _is_operator(user: dict) -> bool:
    settings = get_settings()
    operator_emails = {settings.support_email.lower().strip(), settings.sales_email.lower().strip()}
    return user["email"].lower().strip() in operator_emails


STATUS_LABELS = {
    "open": "Abierto",
    "in_progress": "En gestión",
    "waiting_customer": "Esperando cliente",
    "resolved": "Resuelto",
    "closed": "Cerrado",
}

PRIORITY_LABELS = {
    "low": "Baja",
    "medium": "Media",
    "high": "Alta",
    "critical": "Crítica",
}

CATEGORY_LABELS = {
    "support": "Soporte",
    "billing": "Facturación",
    "access": "Acceso",
    "bug": "Error",
    "integration": "Integración",
}


def _ticket_meta(label: str, value: str) -> str:
    return f"<div class='of-ticket-meta'><span>{label}</span><strong>{value}</strong></div>"


def _support_intro(operator_mode: bool) -> None:
    main_panel = (
        "<div class='of-soft-panel'>"
        "<div class='of-eyebrow'>Soporte que guía la acción</div>"
        "<h3 style='margin:10px 0 10px 0'>Cada ticket debe terminar en un siguiente paso claro</h3>"
        "<p class='of-helper-line'>Esta pantalla debe servirle tanto a un cliente que solo tiene Excel como a un operador que necesita responder rápido y con claridad. Por eso cada acción se explica y cada bloque dice qué pasa después.</p>"
        "<div class='of-support-guide'>"
        "<div class='of-support-guide-card'><strong>1. Explica el caso</strong><p>Describe el bloqueo, el archivo y el resultado esperado para reducir idas y vueltas innecesarias.</p></div>"
        "<div class='of-support-guide-card'><strong>2. Define el estado</strong><p>Marca si el caso sigue en gestión, espera una acción del cliente o ya quedó resuelto.</p></div>"
        "<div class='of-support-guide-card'><strong>3. Decide si notificas</strong><p>Si la respuesta es pública, se puede enviar por correo. Si es nota interna, el cliente no recibe nada.</p></div>"
        "</div>"
        "</div>"
    )
    side_panel = (
        "<div class='of-soft-panel'>"
        "<div class='of-eyebrow'>Regla operativa</div>"
        f"<p class='of-helper-line'>{'Como operador puedes responder, dejar notas internas y cambiar estados desde esta misma vista.' if operator_mode else 'Como cliente puedes abrir tickets, agregar contexto y seguir cada respuesta sin salir de la app.'}</p>"
        "<div class='of-action-note'><strong>Correo al cliente:</strong> solo se envía cuando la respuesta no es interna y la opción de notificación queda activada.</div>"
        "</div>"
    )
    st.markdown(f"<div class='of-support-hero'>{main_panel}{side_panel}</div>", unsafe_allow_html=True)


def _render_operator_guidance() -> None:
    st.markdown(
        "<div class='of-operator-banner'><strong>Modo operador activo.</strong> Para enviar correo al cliente, escribe una respuesta pública y deja marcada la notificación. Si marcas nota interna, el texto se guarda solo para el equipo y el correo se desactiva automáticamente.</div>",
        unsafe_allow_html=True,
    )


def _render_ticket_thread(ticket: dict, user: dict, *, operator_mode: bool = False) -> None:
    meta_cards = [
        _ticket_meta("Estado", STATUS_LABELS.get(ticket["status"], ticket["status"])),
        _ticket_meta("Prioridad", PRIORITY_LABELS.get(ticket["priority"], ticket["priority"])),
        _ticket_meta("Categoría", CATEGORY_LABELS.get(ticket["category"], ticket["category"])),
        _ticket_meta("Origen", ticket["source"]),
        _ticket_meta("Solicitante", f"{ticket['requester_name']} · {ticket['requester_email']}"),
        _ticket_meta("Creado", str(ticket["created_at"])),
    ]
    if ticket.get("company_name"):
        meta_cards.append(_ticket_meta("Empresa", ticket["company_name"]))
    st.markdown(f"<div class='of-ticket-meta-grid'>{''.join(meta_cards)}</div>", unsafe_allow_html=True)

    messages = list_ticket_messages(ticket['id'])
    if messages:
        items: list[str] = []
        for msg in messages:
            author = f"{msg['author_name']} ({msg['author_email']})"
            label = "Nota interna" if msg['is_internal'] else "Mensaje público"
            css_class = "of-thread-item internal" if msg["is_internal"] else "of-thread-item"
            items.append(
                f"<div class='{css_class}'><div class='of-thread-head'><strong>{label} · {author}</strong><span>{msg['created_at']}</span></div><div class='of-thread-body'>{msg['body']}</div></div>"
            )
        st.markdown(f"<div class='of-thread-stack'>{''.join(items)}</div>", unsafe_allow_html=True)
    else:
        st.info("Este ticket todavía no tiene respuestas registradas.")

    if operator_mode:
        st.markdown(
            "<div class='of-action-note'><strong>Cómo responder bien:</strong> si el cliente debe recibir correo, escribe una respuesta pública y deja activa la notificación. Si solo estás documentando contexto interno, marca nota interna. Si cambias solo el estado, el sistema puede notificar ese cambio sin agregar texto.</div>",
            unsafe_allow_html=True,
        )
        with st.form(f"operator_ticket_{ticket['id']}", clear_on_submit=True):
            status = st.selectbox(
                "Nuevo estado del ticket",
                ["open", "in_progress", "waiting_customer", "resolved", "closed"],
                index=["open", "in_progress", "waiting_customer", "resolved", "closed"].index(ticket['status'])
                if ticket['status'] in {"open", "in_progress", "waiting_customer", "resolved", "closed"}
                else 0,
                format_func=lambda value: STATUS_LABELS.get(value, value),
                key=f"status_{ticket['id']}",
            )
            internal_note = st.checkbox(
                "Guardar como nota interna",
                key=f"internal_{ticket['id']}",
                help="Usa esta opción cuando el texto no debe salir al cliente. Al activarla, el correo al cliente se apaga automáticamente.",
            )
            notify_customer = st.checkbox(
                "Enviar correo al cliente con esta gestión",
                value=not internal_note,
                disabled=internal_note,
                help="Déjala activa cuando quieras que el cliente reciba por email la respuesta o el cambio de estado.",
                key=f"notify_{ticket['id']}",
            )
            reply = st.text_area(
                "Respuesta operativa visible para el cliente",
                height=160,
                key=f"reply_{ticket['id']}",
                placeholder="Ejemplo: revisamos tu archivo y falta la columna sku. Vuelve a cargarlo con esa columna o descarga la plantilla desde la sección Plantillas.",
            )
            st.caption("Si este campo queda vacío y solo cambias el estado, se guardará únicamente el cambio de estado.")
            submitted = st.form_submit_button("Guardar gestión y aplicar acción", use_container_width=True)

        if submitted:
            status_changed = status != ticket['status']
            if not reply.strip() and not status_changed:
                st.error("Debes agregar una respuesta o cambiar el estado del ticket.")
            else:
                if reply.strip():
                    add_ticket_message(
                        ticket['id'],
                        user['full_name'],
                        user['email'],
                        reply,
                        is_internal=internal_note,
                        notify_customer=notify_customer,
                        new_status=status,
                    )
                elif status_changed:
                    update_ticket_status(
                        ticket['id'],
                        status,
                        actor_name=user['full_name'],
                        actor_email=user['email'],
                        notify_customer=notify_customer,
                    )
                st.success("Gestión operativa guardada correctamente.")
                st.rerun()
    else:
        with st.form(f"reply_ticket_{ticket['id']}", clear_on_submit=True):
            reply = st.text_area(
                "Añadir contexto o responder",
                height=140,
                placeholder="Cuéntanos qué intentaste, qué archivo subiste o qué parte del flujo te bloqueó.",
            )
            st.caption("Tu mensaje se agrega al historial y se notifica al operador para continuar la gestión.")
            sent = st.form_submit_button("Enviar actualización al equipo", use_container_width=True)

        if sent:
            if not reply.strip():
                st.error("La actualización no puede ir vacía.")
            else:
                add_ticket_message(
                    ticket['id'],
                    user['full_name'],
                    user['email'],
                    reply,
                    is_internal=False,
                    notify_customer=False,
                    new_status="open",
                )
                st.success("Actualización agregada al ticket y reenviada al operador.")
                st.rerun()


def render() -> None:
    user = require_login()
    operator_mode = _is_operator(user)

    st.markdown("## 🆘 Soporte y Tickets")
    st.caption("Abre un caso, deja contexto claro y haz seguimiento desde este mismo espacio.")
    _support_intro(operator_mode)
    if operator_mode:
        _render_operator_guidance()

    st.markdown("<div class='of-page-block'>", unsafe_allow_html=True)
    with st.form("support_ticket_create", clear_on_submit=True):
        subject = st.text_input("Asunto del ticket", placeholder="Ejemplo: no pude completar la carga de inventario")
        category = st.selectbox(
            "Categoría",
            ["support", "billing", "access", "bug", "integration"],
            format_func=lambda value: CATEGORY_LABELS.get(value, value),
        )
        priority = st.selectbox(
            "Prioridad",
            ["low", "medium", "high", "critical"],
            index=1,
            format_func=lambda value: PRIORITY_LABELS.get(value, value),
        )
        message = st.text_area(
            "Describe el problema o la solicitud",
            height=170,
            placeholder="Explica qué intentaste, qué esperabas que pasara y qué ocurrió realmente. Si aplica, menciona el archivo o la sección de la app.",
        )
        st.caption("Entre más claro quede el contexto, más rápido puede responder el equipo sin pedirte varias aclaraciones.")
        submitted = st.form_submit_button("Crear ticket y enviarlo a soporte", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        if not subject.strip() or not message.strip():
            st.error("Debes completar asunto y descripción para crear el ticket.")
        else:
            ticket = create_support_ticket(
                requester_name=user["full_name"],
                requester_email=user["email"],
                company_name=user["company_name"],
                tenant_id=user["tenant_id"],
                subject=subject,
                message=message,
                category=category,
                priority=priority,
                source="app",
            )
            st.success(f"Ticket #{ticket['id']} creado y notificado al equipo de soporte.")
            st.rerun()

    tickets = list_support_tickets(tenant_id=user["tenant_id"], requester_email=user["email"])
    if not tickets:
        st.info("Todavía no has creado tickets desde esta cuenta.")
    else:
        st.markdown("### Tus casos")
        for ticket in tickets:
            label = f"#{ticket['id']} · {ticket['subject']} · {STATUS_LABELS.get(ticket['status'], ticket['status'])} · {PRIORITY_LABELS.get(ticket['priority'], ticket['priority'])}"
            with st.expander(label, expanded=False):
                _render_ticket_thread(ticket, user, operator_mode=False)

    if operator_mode:
        st.divider()
        st.markdown("### Vista operativa")
        all_tickets = list_support_tickets()
        if not all_tickets:
            st.info("Todavía no hay tickets globales para gestionar.")
            return

        status_filter = st.selectbox(
            "Filtrar por estado",
            ["all", "open", "in_progress", "waiting_customer", "resolved", "closed"],
            format_func=lambda value: "Todos" if value == "all" else STATUS_LABELS.get(value, value),
        )
        filtered = [ticket for ticket in all_tickets if status_filter == "all" or ticket["status"] == status_filter]
        for ticket in filtered:
            label = (
                f"#{ticket['id']} · {ticket['subject']} · {STATUS_LABELS.get(ticket['status'], ticket['status'])} · "
                f"{PRIORITY_LABELS.get(ticket['priority'], ticket['priority'])} · {ticket['requester_email']}"
            )
            with st.expander(label, expanded=False):
                _render_ticket_thread(ticket, user, operator_mode=True)