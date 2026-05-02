"""Servicios de soporte y tickets sin acoplar la UI al correo o a la persistencia."""
from __future__ import annotations

from sqlalchemy import select

from core.config import get_settings
from core.database import session_scope
from core.mail import (
    send_support_ticket_created_to_customer,
    send_support_ticket_created_to_operator,
    send_support_ticket_reply_to_customer,
)
from core.models import SupportTicket, SupportTicketMessage


def create_support_ticket(
    requester_name: str,
    requester_email: str,
    subject: str,
    message: str,
    *,
    company_name: str | None = None,
    tenant_id: int | None = None,
    category: str = "support",
    priority: str = "medium",
    source: str = "portal",
) -> dict:
    with session_scope(tenant_id=tenant_id) as db:
        ticket = SupportTicket(
            tenant_id=tenant_id,
            requester_name=requester_name.strip(),
            requester_email=requester_email.lower().strip(),
            company_name=(company_name or "").strip() or None,
            subject=subject.strip(),
            category=category,
            priority=priority,
            status="open",
            source=source,
        )
        db.add(ticket)
        db.flush()

        first_message = SupportTicketMessage(
            ticket_id=ticket.id,
            author_name=requester_name.strip(),
            author_email=requester_email.lower().strip(),
            body=message.strip(),
            is_internal=False,
        )
        db.add(first_message)
        db.flush()
        payload = {
            "id": ticket.id,
            "requester_name": ticket.requester_name,
            "requester_email": ticket.requester_email,
            "company_name": ticket.company_name,
            "subject": ticket.subject,
            "status": ticket.status,
            "message": first_message.body,
        }

    settings = get_settings()
    send_support_ticket_created_to_customer(payload["requester_email"], payload["requester_name"], payload["id"], payload["subject"])
    send_support_ticket_created_to_operator(
        settings.support_email,
        payload["id"],
        payload["requester_name"],
        payload["requester_email"],
        payload["subject"],
        payload["message"],
        payload["company_name"],
    )
    return payload


def add_ticket_message(
    ticket_id: int,
    author_name: str,
    author_email: str,
    body: str,
    *,
    is_internal: bool = False,
    notify_customer: bool = False,
    new_status: str | None = None,
) -> None:
    customer_payload: dict | None = None
    with session_scope() as db:
        ticket = db.get(SupportTicket, ticket_id)
        if not ticket:
            raise ValueError(f"Ticket no encontrado: {ticket_id}")

        message = SupportTicketMessage(
            ticket_id=ticket_id,
            author_name=author_name.strip(),
            author_email=author_email.lower().strip(),
            body=body.strip(),
            is_internal=is_internal,
        )
        db.add(message)
        if new_status:
            ticket.status = new_status

        customer_payload = {
            "email": ticket.requester_email,
            "name": ticket.requester_name,
            "subject": ticket.subject,
            "body": body.strip(),
        }

    if notify_customer and customer_payload:
        send_support_ticket_reply_to_customer(
            customer_payload["email"],
            customer_payload["name"],
            ticket_id,
            customer_payload["subject"],
            customer_payload["body"],
        )


def list_support_tickets(*, tenant_id: int | None = None, requester_email: str | None = None) -> list[dict]:
    with session_scope(tenant_id=tenant_id) as db:
        stmt = select(SupportTicket).order_by(SupportTicket.created_at.desc())
        if tenant_id is not None:
            stmt = stmt.where(SupportTicket.tenant_id == tenant_id)
        if requester_email:
            stmt = stmt.where(SupportTicket.requester_email == requester_email.lower().strip())

        rows = db.scalars(stmt).all()
        return [
            {
                "id": row.id,
                "tenant_id": row.tenant_id,
                "requester_name": row.requester_name,
                "requester_email": row.requester_email,
                "company_name": row.company_name,
                "subject": row.subject,
                "category": row.category,
                "priority": row.priority,
                "status": row.status,
                "source": row.source,
                "created_at": row.created_at,
                "updated_at": row.updated_at,
            }
            for row in rows
        ]


def list_ticket_messages(ticket_id: int) -> list[dict]:
    with session_scope() as db:
        rows = db.scalars(
            select(SupportTicketMessage)
            .where(SupportTicketMessage.ticket_id == ticket_id)
            .order_by(SupportTicketMessage.created_at.asc())
        ).all()
        return [
            {
                "id": row.id,
                "author_name": row.author_name,
                "author_email": row.author_email,
                "body": row.body,
                "is_internal": row.is_internal,
                "created_at": row.created_at,
            }
            for row in rows
        ]