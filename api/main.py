"""FastAPI entrypoint para OptiFerre SaaS."""
from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import (
    assistant,
    analysis,
    auth,
    billing,
    dashboard,
    inventory,
    products,
    purchase_orders,
    support,
    templates,
)


def _allowed_origins() -> list[str]:
    raw = os.getenv("API_CORS_ORIGINS", "http://localhost:3000")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def create_app() -> FastAPI:
    app = FastAPI(
        title="OptiFerre API",
        version="1.0.0",
        description="API REST de OptiFerre. Lógica reutilizada de core/, services/ y engine/.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_allowed_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(assistant.router, prefix="/assistant", tags=["assistant"])
    app.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
    app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
    app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
    app.include_router(products.router, prefix="/products", tags=["products"])
    app.include_router(purchase_orders.router, prefix="/purchase-orders", tags=["purchase-orders"])
    app.include_router(billing.router, prefix="/billing", tags=["billing"])
    app.include_router(support.router, prefix="/support", tags=["support"])
    app.include_router(templates.router, prefix="/templates", tags=["templates"])

    @app.get("/health", tags=["meta"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
