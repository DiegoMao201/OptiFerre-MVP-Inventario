"""Modelos ORM: Tenant, User, Subscription, AnalysisRun + AI/POs/Snapshots."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    company_name: Mapped[str] = mapped_column(String(120))
    brand_primary_color: Mapped[str] = mapped_column(String(16), default="#FF6B1A")
    brand_logo_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    theme_mode: Mapped[str] = mapped_column(String(8), default="dark")  # dark | light
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    users: Mapped[list["User"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    subscription: Mapped[Optional["Subscription"]] = relationship(
        back_populates="tenant", uselist=False, cascade="all, delete-orphan"
    )
    runs: Mapped[list["AnalysisRun"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"))
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(32), default="owner")  # owner | analyst | viewer
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    tenant: Mapped[Tenant] = relationship(back_populates="users")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), unique=True)
    plan: Mapped[str] = mapped_column(String(32), default="trial")  # trial|starter|pro|enterprise
    status: Mapped[str] = mapped_column(String(32), default="trialing")  # trialing|active|past_due|canceled
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    stripe_subscription_id: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    current_period_end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    trial_ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    tenant: Mapped[Tenant] = relationship(back_populates="subscription")

    def is_active(self) -> bool:
        if self.status in {"active", "trialing"}:
            if self.status == "trialing" and self.trial_ends_at:
                return datetime.utcnow() <= self.trial_ends_at
            return True
        return False


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"))
    user_email: Mapped[str] = mapped_column(String(180))
    rows_inventory: Mapped[int] = mapped_column(Integer, default=0)
    rows_sales: Mapped[int] = mapped_column(Integer, default=0)
    capital_total: Mapped[float] = mapped_column(default=0.0)
    capital_inmovilizado: Mapped[float] = mapped_column(default=0.0)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    tenant: Mapped[Tenant] = relationship(back_populates="runs")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"))
    user_email: Mapped[Optional[str]] = mapped_column(String(180), nullable=True)
    action: Mapped[str] = mapped_column(String(120))
    entity: Mapped[str] = mapped_column(String(120), default="system")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=True)
    requester_name: Mapped[str] = mapped_column(String(120))
    requester_email: Mapped[str] = mapped_column(String(180), index=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    subject: Mapped[str] = mapped_column(String(180))
    category: Mapped[str] = mapped_column(String(32), default="support")
    priority: Mapped[str] = mapped_column(String(16), default="medium")
    status: Mapped[str] = mapped_column(String(24), default="open")
    source: Mapped[str] = mapped_column(String(24), default="portal")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    tenant: Mapped[Optional[Tenant]] = relationship()
    messages: Mapped[list["SupportTicketMessage"]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan"
    )


class SupportTicketMessage(Base):
    __tablename__ = "support_ticket_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("support_tickets.id", ondelete="CASCADE"))
    author_name: Mapped[str] = mapped_column(String(120))
    author_email: Mapped[str] = mapped_column(String(180))
    body: Mapped[str] = mapped_column(Text)
    is_internal: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    ticket: Mapped[SupportTicket] = relationship(back_populates="messages")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


# ---------------------------------------------------------------------------
# Persistencia accionable: snapshots, sugerencias editables, órdenes de compra
# ---------------------------------------------------------------------------


class InventorySnapshot(Base):
    """Última foto del inventario por SKU para un tenant.

    Se actualiza vía UPSERT en cada carga. Permite que la IA Pro/Enterprise
    razone sobre datos reales sin depender de la sesión Streamlit.
    """

    __tablename__ = "inventory_snapshots"
    __table_args__ = (
        UniqueConstraint("tenant_id", "sku", name="uq_inventory_snapshots_tenant_sku"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), index=True
    )
    sku: Mapped[str] = mapped_column(String(80), index=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    on_hand: Mapped[float] = mapped_column(Float, default=0.0)
    avg_cost: Mapped[float] = mapped_column(Float, default=0.0)
    lead_time_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    pack_size: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class SalesSnapshot(Base):
    """Resumen agregado de ventas por SKU dentro de un período."""

    __tablename__ = "sales_snapshots"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "sku", "period_start", "period_end",
            name="uq_sales_snapshots_tenant_sku_period",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), index=True
    )
    sku: Mapped[str] = mapped_column(String(80), index=True)
    period_start: Mapped[datetime] = mapped_column(DateTime)
    period_end: Mapped[datetime] = mapped_column(DateTime)
    units_sold: Mapped[float] = mapped_column(Float, default=0.0)
    revenue: Mapped[float] = mapped_column(Float, default=0.0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class PurchaseSuggestion(Base):
    """Sugerencia de compra editable por SKU.

    qty_ai → lo que recomendó el motor.
    qty_user → ajuste manual del operador (UPSERT).
    included → si entra en la próxima orden.
    """

    __tablename__ = "purchase_suggestions"
    __table_args__ = (
        UniqueConstraint("tenant_id", "sku", name="uq_purchase_suggestions_tenant_sku"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), index=True
    )
    run_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="SET NULL"), nullable=True
    )
    sku: Mapped[str] = mapped_column(String(80), index=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    qty_ai: Mapped[float] = mapped_column(Float, default=0.0)
    qty_user: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unit_cost: Mapped[float] = mapped_column(Float, default=0.0)
    included: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    updated_by: Mapped[Optional[str]] = mapped_column(String(180), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    @property
    def effective_qty(self) -> float:
        return float(self.qty_user) if self.qty_user is not None else float(self.qty_ai)


class PurchaseOrder(Base):
    """Cabecera de una orden de compra generada desde sugerencias."""

    __tablename__ = "purchase_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), index=True
    )
    code: Mapped[str] = mapped_column(String(40), index=True)
    status: Mapped[str] = mapped_column(String(24), default="draft")  # draft|sent|done|canceled
    total_amount: Mapped[float] = mapped_column(Float, default=0.0)
    total_units: Mapped[float] = mapped_column(Float, default=0.0)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by: Mapped[Optional[str]] = mapped_column(String(180), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    items: Mapped[list["PurchaseOrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_orders.id", ondelete="CASCADE"), index=True
    )
    sku: Mapped[str] = mapped_column(String(80))
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    qty: Mapped[float] = mapped_column(Float, default=0.0)
    unit_cost: Mapped[float] = mapped_column(Float, default=0.0)
    line_total: Mapped[float] = mapped_column(Float, default=0.0)

    order: Mapped[PurchaseOrder] = relationship(back_populates="items")


# ---------------------------------------------------------------------------
# IA: hilos de chat persistentes + auditoría de acciones
# ---------------------------------------------------------------------------


class AIConversation(Base):
    __tablename__ = "ai_conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    plan: Mapped[str] = mapped_column(String(32), default="starter")
    title: Mapped[str] = mapped_column(String(180), default="Nueva conversación")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    messages: Mapped[list["AIMessage"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan", order_by="AIMessage.id"
    )


class AIMessage(Base):
    __tablename__ = "ai_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("ai_conversations.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[str] = mapped_column(String(16))  # system|user|assistant|tool
    content: Mapped[str] = mapped_column(Text)
    tool_call_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tokens_in: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tokens_out: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    conversation: Mapped[AIConversation] = relationship(back_populates="messages")


class AIActionLog(Base):
    """Auditoría de acciones ejecutadas por la IA (function calling)."""

    __tablename__ = "ai_action_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    conversation_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("ai_conversations.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(80))
    payload: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(24), default="ok")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
