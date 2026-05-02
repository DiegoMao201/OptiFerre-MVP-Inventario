"""Support tickets and messages.

Revision ID: 20260502_0002
Revises: 20260502_0001
Create Date: 2026-05-02 17:00:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260502_0002"
down_revision = "20260502_0001"
branch_labels = None
depends_on = None


def _table_exists(inspector: sa.Inspector, table_name: str) -> bool:
    return table_name in inspector.get_table_names()


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _table_exists(inspector, "support_tickets"):
        op.create_table(
            "support_tickets",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=True),
            sa.Column("requester_name", sa.String(length=120), nullable=False),
            sa.Column("requester_email", sa.String(length=180), nullable=False),
            sa.Column("company_name", sa.String(length=120), nullable=True),
            sa.Column("subject", sa.String(length=180), nullable=False),
            sa.Column("category", sa.String(length=32), nullable=False, server_default="support"),
            sa.Column("priority", sa.String(length=16), nullable=False, server_default="medium"),
            sa.Column("status", sa.String(length=24), nullable=False, server_default="open"),
            sa.Column("source", sa.String(length=24), nullable=False, server_default="portal"),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
            sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        )
        op.create_index("ix_support_tickets_requester_email", "support_tickets", ["requester_email"], unique=False)

    inspector = sa.inspect(bind)
    if not _table_exists(inspector, "support_ticket_messages"):
        op.create_table(
            "support_ticket_messages",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("ticket_id", sa.Integer(), sa.ForeignKey("support_tickets.id", ondelete="CASCADE"), nullable=False),
            sa.Column("author_name", sa.String(length=120), nullable=False),
            sa.Column("author_email", sa.String(length=180), nullable=False),
            sa.Column("body", sa.Text(), nullable=False),
            sa.Column("is_internal", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if _table_exists(inspector, "support_ticket_messages"):
        op.drop_table("support_ticket_messages")
        inspector = sa.inspect(bind)
    if _table_exists(inspector, "support_tickets"):
        op.drop_index("ix_support_tickets_requester_email", table_name="support_tickets")
        op.drop_table("support_tickets")