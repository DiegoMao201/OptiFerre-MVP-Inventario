"""Structured logging with tenant/user context for production debugging."""
from __future__ import annotations

import json
import logging
import sys
from contextvars import ContextVar, Token
from datetime import datetime, timezone

tenant_context: ContextVar[int | None] = ContextVar("tenant_id", default=None)
user_context: ContextVar[int | None] = ContextVar("user_id", default=None)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "tenant_id": getattr(record, "tenant_id", None) or tenant_context.get(),
            "user_id": getattr(record, "user_id", None) or user_context.get(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=True)


def configure_logging() -> None:
    root = logging.getLogger()
    if getattr(configure_logging, "_configured", False):
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root.handlers = [handler]
    root.setLevel(logging.INFO)
    configure_logging._configured = True  # type: ignore[attr-defined]


def set_log_context(tenant_id: int | None = None, user_id: int | None = None) -> tuple[Token, Token]:
    tenant_token = tenant_context.set(tenant_id)
    user_token = user_context.set(user_id)
    return tenant_token, user_token


def clear_log_context(
    tenant_token: Token | None = None,
    user_token: Token | None = None,
) -> None:
    if tenant_token is not None:
        tenant_context.reset(tenant_token)
    else:
        tenant_context.set(None)

    if user_token is not None:
        user_context.reset(user_token)
    else:
        user_context.set(None)