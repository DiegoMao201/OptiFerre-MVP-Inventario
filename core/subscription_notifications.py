"""Recordatorios y nudges de suscripción para ejecución programada."""
from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import select

from core.config import get_settings
from core.database import session_scope
from core.mail import (
    send_payment_due_email,
    send_trial_ending_email,
    send_upgrade_nudge_email,
)
from core.models import Subscription, Tenant, User


def run_billing_notification_cycle() -> dict:
    settings = get_settings()
    now = datetime.utcnow()
    trial_threshold = now + timedelta(days=settings.billing_reminder_days_before_trial_end)
    renewal_threshold = now + timedelta(days=settings.billing_reminder_days_before_renewal)
    summary = {"trial_ending": 0, "payment_due": 0, "upgrade_nudge": 0}

    with session_scope() as db:
        subscriptions = db.scalars(select(Subscription)).all()
        for subscription in subscriptions:
            tenant = db.get(Tenant, subscription.tenant_id)
            user = db.scalar(select(User).where(User.tenant_id == subscription.tenant_id).order_by(User.id.asc()))
            if not tenant or not user:
                continue

            billing_url = settings.base_url.rstrip("/") + "/"
            if subscription.status == "trialing" and subscription.trial_ends_at and now <= subscription.trial_ends_at <= trial_threshold:
                days_left = max(0, int((subscription.trial_ends_at - now).total_seconds() // 86400))
                send_trial_ending_email(user.email, user.full_name, tenant.company_name, days_left, billing_url)
                summary["trial_ending"] += 1

            if subscription.status == "past_due":
                send_payment_due_email(user.email, user.full_name, tenant.company_name, subscription.plan, billing_url)
                summary["payment_due"] += 1

            if subscription.status == "active" and subscription.current_period_end and now <= subscription.current_period_end <= renewal_threshold:
                send_upgrade_nudge_email(user.email, user.full_name, tenant.company_name, subscription.plan, billing_url)
                summary["upgrade_nudge"] += 1

    return summary
