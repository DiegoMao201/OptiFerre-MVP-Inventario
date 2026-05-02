"""Capa de persistencia: engine SQLAlchemy + sesión scoped."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import logging

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from core.config import get_settings
from core.logging_config import clear_log_context, set_log_context


class Base(DeclarativeBase):
    """Base declarativa para todos los modelos ORM."""


_settings = get_settings()
_engine_kwargs = {"future": True, "pool_pre_ping": True}
if _settings.database_url.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(_settings.database_url, **_engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
logger = logging.getLogger("optiferre.database")


def init_db() -> None:
    """Crea las tablas si no existen."""
    from core import models  # noqa: F401  (registra modelos)

    Base.metadata.create_all(engine)


@contextmanager
def session_scope(*, tenant_id: int | None = None, user_id: int | None = None) -> Iterator[Session]:
    """Context manager con commit/rollback automáticos."""
    session = SessionLocal()
    tenant_token = None
    user_token = None
    session.info["tenant_id"] = tenant_id
    session.info["user_id"] = user_id
    if tenant_id is not None or user_id is not None:
        tenant_token, user_token = set_log_context(tenant_id=tenant_id, user_id=user_id)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        logger.exception(
            "database_session_error",
            extra={"tenant_id": tenant_id, "user_id": user_id},
        )
        raise
    finally:
        session.close()
        if tenant_token is not None or user_token is not None:
            clear_log_context(tenant_token=tenant_token, user_token=user_token)


@contextmanager
def tenant_session_scope(tenant_id: int, user_id: int | None = None) -> Iterator[Session]:
    """Wrapper explícito para consultas ligadas obligatoriamente a un tenant."""
    with session_scope(tenant_id=tenant_id, user_id=user_id) as session:
        yield session


def tenant_select(session: Session, model: type[Base]):
    """Genera un select forzado al tenant_id actual de la sesión."""
    tenant_id = session.info.get("tenant_id")
    if tenant_id is None:
        raise ValueError("tenant_select requiere una sesión tenant-aware")
    if not hasattr(model, "tenant_id"):
        raise ValueError(f"{model.__name__} no soporta filtrado por tenant_id")
    return select(model).where(getattr(model, "tenant_id") == tenant_id)


def tenant_get(session: Session, model: type[Base], row_id: int):
    """Obtiene una fila por PK restringida al tenant actual."""
    stmt = tenant_select(session, model).where(getattr(model, "id") == row_id)
    return session.scalar(stmt)
