"""Carga centralizada de configuración desde variables de entorno."""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except Exception:  # pragma: no cover
    pass


def _normalize_database_url(raw_url: str) -> str:
    """Normaliza aliases comunes para SQLAlchemy en producción."""
    if raw_url.startswith("postgres://"):
        return raw_url.replace("postgres://", "postgresql+psycopg2://", 1)
    if raw_url.startswith("postgresql://") and "+" not in raw_url.split("://", 1)[0]:
        return raw_url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return raw_url


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_env: str
    secret_key: str
    base_url: str
    database_url: str
    mail_provider: str
    mail_from_name: str
    mail_from_email: str
    mail_reply_to: str
    sendgrid_api_key: str
    stripe_secret_key: str
    stripe_publishable_key: str
    stripe_webhook_secret: str
    stripe_price_starter: str
    stripe_price_pro: str
    stripe_price_enterprise: str
    sales_email: str
    sales_phone: str

    @property
    def stripe_enabled(self) -> bool:
        return bool(self.stripe_secret_key) and not self.stripe_secret_key.endswith("xxx")

    @property
    def mail_enabled(self) -> bool:
        if self.mail_provider != "sendgrid":
            return False
        return bool(self.sendgrid_api_key and self.mail_from_email)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    database_url = _normalize_database_url(os.getenv("DATABASE_URL", "sqlite:///optiferre.db"))
    return Settings(
        app_name=os.getenv("APP_NAME", "OptiFerre SaaS"),
        app_env=os.getenv("APP_ENV", "development"),
        secret_key=os.getenv("APP_SECRET_KEY", "dev-secret-change-me"),
        base_url=os.getenv("APP_BASE_URL", "http://localhost:8501"),
        database_url=database_url,
        mail_provider=os.getenv("MAIL_PROVIDER", "sendgrid").strip().lower(),
        mail_from_name=os.getenv("MAIL_FROM_NAME", "Nexus Pro").strip(),
        mail_from_email=os.getenv("MAIL_FROM_EMAIL", "").strip(),
        mail_reply_to=os.getenv("MAIL_REPLY_TO", "").strip(),
        sendgrid_api_key=os.getenv("SENDGRID_API_KEY", "").strip(),
        stripe_secret_key=os.getenv("STRIPE_SECRET_KEY", ""),
        stripe_publishable_key=os.getenv("STRIPE_PUBLISHABLE_KEY", ""),
        stripe_webhook_secret=os.getenv("STRIPE_WEBHOOK_SECRET", ""),
        stripe_price_starter=os.getenv("STRIPE_PRICE_STARTER", ""),
        stripe_price_pro=os.getenv("STRIPE_PRICE_PRO", ""),
        stripe_price_enterprise=os.getenv("STRIPE_PRICE_ENTERPRISE", ""),
        sales_email=os.getenv("SALES_CONTACT_EMAIL", "diegomao.201@gmail.com"),
        sales_phone=os.getenv("SALES_CONTACT_PHONE", "+57 300 000 0000"),
    )
