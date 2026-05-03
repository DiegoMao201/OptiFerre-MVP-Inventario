"""Endpoints de soporte y tickets."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from api.deps.security import get_current_user
from core.support import add_ticket_message, create_support_ticket, list_support_tickets, list_ticket_messages

router = APIRouter()


class TicketCreateRequest(BaseModel):
    subject: str = Field(..., min_length=4, max_length=180)
    message: str = Field(..., min_length=10, max_length=5000)
    category: str = Field(default="support", max_length=32)
    priority: str = Field(default="medium", max_length=16)


class TicketReplyRequest(BaseModel):
    body: str = Field(..., min_length=2, max_length=5000)


def _get_visible_ticket(ticket_id: int, current_user: dict) -> dict:
    tickets = list_support_tickets(
        tenant_id=current_user["tenant_id"],
        requester_email=current_user["email"],
    )
    ticket = next((row for row in tickets if row["id"] == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket no encontrado.")
    return ticket


@router.get("/tickets")
def tickets(current_user: dict = Depends(get_current_user)) -> dict:
    return {
        "items": list_support_tickets(
            tenant_id=current_user["tenant_id"],
            requester_email=current_user["email"],
        )
    }


@router.post("/tickets", status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreateRequest, current_user: dict = Depends(get_current_user)) -> dict:
    ticket = create_support_ticket(
        requester_name=current_user["full_name"],
        requester_email=current_user["email"],
        company_name=current_user["company_name"],
        tenant_id=current_user["tenant_id"],
        subject=payload.subject,
        message=payload.message,
        category=payload.category,
        priority=payload.priority,
    )
    return {"ticket": ticket}


@router.get("/tickets/{ticket_id}")
def ticket_detail(ticket_id: int, current_user: dict = Depends(get_current_user)) -> dict:
    ticket = _get_visible_ticket(ticket_id, current_user)
    return {"ticket": ticket, "messages": list_ticket_messages(ticket_id)}


@router.post("/tickets/{ticket_id}/messages")
def reply_ticket(ticket_id: int, payload: TicketReplyRequest, current_user: dict = Depends(get_current_user)) -> dict:
    ticket = _get_visible_ticket(ticket_id, current_user)
    add_ticket_message(
        ticket_id,
        current_user["full_name"],
        current_user["email"],
        payload.body,
        is_internal=False,
        notify_customer=False,
        new_status="open",
    )
    return {"ticket": ticket, "messages": list_ticket_messages(ticket_id)}