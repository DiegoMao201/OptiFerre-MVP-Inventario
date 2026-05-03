"""AI persistence + actionable purchase orders + snapshots.

Revision ID: 20260502_0004
Revises: 20260502_0003
Create Date: 2026-05-02 18:00:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260502_0004"
down_revision = "20260502_0003"
branch_labels = None
depends_on = None


def _table_exists(inspector: sa.Inspector, name: str) -> bool:
    return name in inspector.get_table_names()


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _table_exists(inspector, "inventory_snapshots"):
        op.create_table(
            "inventory_snapshots",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True),
            sa.Column("sku", sa.String(length=80), nullable=False, index=True),
            sa.Column("name", sa.String(length=255), nullable=True),
            sa.Column("category", sa.String(length=120), nullable=True),
            sa.Column("on_hand", sa.Float(), nullable=False, server_default="0"),
            sa.Column("avg_cost", sa.Float(), nullable=False, server_default="0"),
            sa.Column("lead_time_days", sa.Float(), nullable=True),
            sa.Column("pack_size", sa.Float(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
            sa.UniqueConstraint("tenant_id", "sku", name="uq_inventory_snapshots_tenant_sku"),
        )

    if not _table_exists(inspector, "sales_snapshots"):
        op.create_table(
            "sales_snapshots",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True),
            sa.Column("sku", sa.String(length=80), nullable=False, index=True),
            sa.Column("period_start", sa.DateTime(), nullable=False),
            sa.Column("period_end", sa.DateTime(), nullable=False),
            sa.Column("units_sold", sa.Float(), nullable=False, server_default="0"),
            sa.Column("revenue", sa.Float(), nullable=False, server_default="0"),
            sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
            sa.UniqueConstraint("tenant_id", "sku", "period_start", "period_end", name="uq_sales_snapshots_tenant_sku_period"),
        )

    if not _table_exists(inspector, "purchase_suggestions"):
        op.create_table(
            "purchase_suggestions",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True),
            sa.Column("run_id", sa.Integer(), sa.ForeignKey("analysis_runs.id", ondelete="SET NULL"), nullable=True),
            sa.Column("sku", sa.String(length=80), nullable=False, index=True),
            sa.Column("name", sa.String(length=255), nullable=True),
            sa.Column("qty_ai", sa.Float(), nullable=False, server_default="0"),
            sa.Column("qty_user", sa.Float(), nullable=True),
            sa.Column("unit_cost", sa.Float(), nullable=False, server_default="0"),
            sa.Column("included", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("notes", sa.Text(), nullable=True),
            sa.Column("updated_by", sa.String(length=180), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
            sa.UniqueConstraint("tenant_id", "sku", name="uq_purchase_suggestions_tenant_sku"),
        )

    if not _table_exists(inspector, "purchase_orders"):
        op.create_table(
            "purchase_orders",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True),
            sa.Column("code", sa.String(length=40), nullable=False, index=True),
            sa.Column("status", sa.String(length=24), nullable=False, server_default="draft"),
            sa.Column("total_amount", sa.Float(), nullable=False, server_default="0"),
            sa.Column("total_units", sa.Float(), nullable=False, server_default="0"),
            sa.Column("notes", sa.Text(), nullable=True),
            sa.Column("created_by", sa.String(length=180), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        )

    if not _table_exists(inspector, "purchase_order_items"):
        op.create_table(
            "purchase_order_items",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("order_id", sa.Integer(), sa.ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False, index=True),
            sa.Column("sku", sa.String(length=80), nullable=False),
            sa.Column("name", sa.String(length=255), nullable=True),
            sa.Column("qty", sa.Float(), nullable=False, server_default="0"),
            sa.Column("unit_cost", sa.Float(), nullable=False, server_default="0"),
            sa.Column("line_total", sa.Float(), nullable=False, server_default="0"),
        )

    if not _table_exists(inspector, "ai_conversations"):
        op.create_table(
            "ai_conversations",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True),
            sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
            sa.Column("plan", sa.String(length=32), nullable=False, server_default="starter"),
            sa.Column("title", sa.String(length=180), nullable=False, server_default="Nueva conversación"),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
            sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        )

    if not _table_exists(inspector, "ai_messages"):
        op.create_table(
            "ai_messages",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False, index=True),
            sa.Column("role", sa.String(length=16), nullable=False),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column("tool_call_json", sa.Text(), nullable=True),
            sa.Column("tokens_in", sa.Integer(), nullable=True),
            sa.Column("tokens_out", sa.Integer(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        )

    if not _table_exists(inspector, "ai_action_logs"):
        op.create_table(
            "ai_action_logs",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True),
            sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
            sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("ai_conversations.id", ondelete="SET NULL"), nullable=True),
            sa.Column("action", sa.String(length=80), nullable=False),
            sa.Column("payload", sa.JSON(), nullable=True),
            sa.Column("status", sa.String(length=24), nullable=False, server_default="ok"),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        )


def downgrade() -> None:
    for table in (
        "ai_action_logs",
        "ai_messages",
        "ai_conversations",
        "purchase_order_items",
        "purchase_orders",
        "purchase_suggestions",
        "sales_snapshots",
        "inventory_snapshots",
    ):
        op.drop_table(table)
