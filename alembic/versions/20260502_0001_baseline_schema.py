"""Baseline schema for OptiFerre SaaS.

Revision ID: 20260502_0001
Revises:
Create Date: 2026-05-02 16:30:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260502_0001"
down_revision = None
branch_labels = None
depends_on = None


def _table_exists(inspector: sa.Inspector, table_name: str) -> bool:
    return table_name in inspector.get_table_names()


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _table_exists(inspector, "tenants"):
        op.create_table(
            "tenants",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("slug", sa.String(length=64), nullable=False),
            sa.Column("company_name", sa.String(length=120), nullable=False),
            sa.Column("brand_primary_color", sa.String(length=16), nullable=False, server_default="#FF6B1A"),
            sa.Column("brand_logo_url", sa.String(length=512), nullable=True),
            sa.Column("theme_mode", sa.String(length=8), nullable=False, server_default="dark"),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        )
        op.create_index("ix_tenants_slug", "tenants", ["slug"], unique=True)

    if not _table_exists(inspector, "users"):
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
            sa.Column("email", sa.String(length=180), nullable=False),
            sa.Column("password_hash", sa.String(length=255), nullable=False),
            sa.Column("full_name", sa.String(length=120), nullable=False),
            sa.Column("role", sa.String(length=32), nullable=False, server_default="owner"),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        )
        op.create_index("ix_users_email", "users", ["email"], unique=True)

    if not _table_exists(inspector, "subscriptions"):
        op.create_table(
            "subscriptions",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
            sa.Column("plan", sa.String(length=32), nullable=False, server_default="trial"),
            sa.Column("status", sa.String(length=32), nullable=False, server_default="trialing"),
            sa.Column("stripe_customer_id", sa.String(length=120), nullable=True),
            sa.Column("stripe_subscription_id", sa.String(length=120), nullable=True),
            sa.Column("current_period_end", sa.DateTime(), nullable=True),
            sa.Column("trial_ends_at", sa.DateTime(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
            sa.UniqueConstraint("tenant_id", name="uq_subscriptions_tenant_id"),
        )

    if not _table_exists(inspector, "analysis_runs"):
        op.create_table(
            "analysis_runs",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
            sa.Column("user_email", sa.String(length=180), nullable=False),
            sa.Column("rows_inventory", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("rows_sales", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("capital_total", sa.Float(), nullable=False, server_default="0"),
            sa.Column("capital_inmovilizado", sa.Float(), nullable=False, server_default="0"),
            sa.Column("notes", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        )

    if not _table_exists(inspector, "audit_logs"):
        op.create_table(
            "audit_logs",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
            sa.Column("user_email", sa.String(length=180), nullable=True),
            sa.Column("action", sa.String(length=120), nullable=False),
            sa.Column("entity", sa.String(length=120), nullable=False, server_default="system"),
            sa.Column("notes", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    for table_name in ("audit_logs", "analysis_runs", "subscriptions", "users", "tenants"):
        if _table_exists(inspector, table_name):
            op.drop_table(table_name)
            inspector = sa.inspect(bind)