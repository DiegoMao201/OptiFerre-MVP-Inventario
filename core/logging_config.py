"""Structured logging with tenant/user context for production debugging."""
from __future__ import annotations

import json
import logging
import sys
from contextvars import ContextVar
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


def set_log_context(tenant_id: int | None = None, user_id: int | None = None) -> None:
    tenant_context.set(tenant_id)
    user_context.set(user_id)


def clear_log_context() -> None:
    tenant_context.set(None)
    user_context.set(None)