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


def _render_ticket_thread(ticket: dict, user: dict, *, operator_mode: bool = False) -> None:
    st.write(f"Categoria: {ticket['category']}")
    st.write(f"Origen: {ticket['source']}")
    st.write(f"Creado: {ticket['created_at']}")
    st.write(f"Solicitante: {ticket['requester_name']} · {ticket['requester_email']}")
    if ticket.get("company_name"):
        st.write(f"Empresa: {ticket['company_name']}")

    messages = list_ticket_messages(ticket['id'])
    for msg in messages:
        author = f"{msg['author_name']} ({msg['author_email']})"
        label = "Nota interna" if msg['is_internal'] else "Mensaje"
        st.markdown(f"**{label} · {author}**")
        st.write(msg['body'])
        st.caption(f"{msg['created_at']}")

    if operator_mode:
        with st.form(f"operator_ticket_{ticket['id']}", clear_on_submit=True):
            status = st.selectbox(
                "Estado",
                ["open", "in_progress", "waiting_customer", "resolved", "closed"],
                index=["open", "in_progress", "waiting_customer", "resolved", "closed"].index(ticket['status'])
                if ticket['status'] in {"open", "in_progress", "waiting_customer", "resolved", "closed"}
                else 0,
                key=f"status_{ticket['id']}",
            )
            internal_note = st.checkbox("Guardar como nota interna", key=f"internal_{ticket['id']}")
            notify_customer = st.checkbox(
                "Notificar al cliente por correo",
                value=not internal_note,
                disabled=internal_note,
                key=f"notify_{ticket['id']}",
            )
            reply = st.text_area("Respuesta operativa", height=140, key=f"reply_{ticket['id']}")
            submitted = st.form_submit_button("Guardar gestión", use_container_width=True)

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
            reply = st.text_area("Añadir contexto o responder", height=120)
            sent = st.form_submit_button("Enviar actualización", use_container_width=True)

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

    with st.form("support_ticket_create", clear_on_submit=True):
        subject = st.text_input("Asunto del ticket", placeholder="Ejemplo: no pude completar la carga de inventario")
        category = st.selectbox("Categoría", ["support", "billing", "access", "bug", "integration"])
        priority = st.selectbox("Prioridad", ["low", "medium", "high", "critical"], index=1)
        message = st.text_area("Describe el problema o la solicitud", height=160)
        submitted = st.form_submit_button("Crear ticket", use_container_width=True)

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
            label = f"#{ticket['id']} · {ticket['subject']} · {ticket['status'].upper()} · {ticket['priority'].upper()}"
            with st.expander(label, expanded=False):
                _render_ticket_thread(ticket, user, operator_mode=False)

    if operator_mode:
        st.divider()
        st.markdown("### Vista operativa")
        all_tickets = list_support_tickets()
        if not all_tickets:
            st.info("Todavía no hay tickets globales para gestionar.")
            return

        status_filter = st.selectbox("Filtrar por estado", ["all", "open", "in_progress", "waiting_customer", "resolved", "closed"])
        filtered = [ticket for ticket in all_tickets if status_filter == "all" or ticket["status"] == status_filter]
        for ticket in filtered:
            label = (
                f"#{ticket['id']} · {ticket['subject']} · {ticket['status'].upper()} · "
                f"{ticket['priority'].upper()} · {ticket['requester_email']}"
            )
            with st.expander(label, expanded=False):
                _render_ticket_thread(ticket, user, operator_mode=True)