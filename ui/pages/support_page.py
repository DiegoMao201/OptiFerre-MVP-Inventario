"""Página privada de soporte y tickets para clientes autenticados."""
from __future__ import annotations

import streamlit as st

from core.auth import require_login
from core.support import add_ticket_message, create_support_ticket, list_support_tickets, list_ticket_messages


def render() -> None:
    user = require_login()

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
        return

    st.markdown("### Tus casos")
    for ticket in tickets:
        label = f"#{ticket['id']} · {ticket['subject']} · {ticket['status'].upper()} · {ticket['priority'].upper()}"
        with st.expander(label, expanded=False):
            st.write(f"Categoria: {ticket['category']}")
            st.write(f"Origen: {ticket['source']}")
            st.write(f"Creado: {ticket['created_at']}")
            messages = list_ticket_messages(ticket['id'])
            for msg in messages:
                author = f"{msg['author_name']} ({msg['author_email']})"
                st.markdown(f"**{author}**")
                st.write(msg['body'])
                st.caption(f"{msg['created_at']}")

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
                        new_status="waiting_customer",
                    )
                    st.success("Actualización agregada al ticket.")
                    st.rerun()