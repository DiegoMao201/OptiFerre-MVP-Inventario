"""Catálogo central de planes, jerarquía RBAC y matriz de features.

Single source of truth. Tanto billing como UI, AI factory y middleware
deben leer desde aquí para evitar inconsistencias.
"""
from __future__ import annotations

from typing import Iterable

# Jerarquía: trial debe heredar features de Pro durante el período de prueba
# para dejar al usuario evaluar el producto completo. Starter es el plan más
# bajo de pago. Cada nivel desbloquea acumulativamente funciones.
PLAN_RANK: dict[str, int] = {
    "free": 0,
    "starter": 1,
    "trial": 2,    # trial se trata como Pro mientras está vigente
    "pro": 2,
    "enterprise": 3,
}

PLAN_KEYS: tuple[str, ...] = ("starter", "pro", "enterprise")


PLAN_CATALOG: dict[str, dict] = {
    "starter": {
        "name": "Starter",
        "tagline": "El Concierge",
        "price_monthly_usd": 15,
        "ai_persona": "concierge",
        "ai_persona_label": "Concierge Onboarding",
        "summary": (
            "Bienvenida guiada, mapeo de columnas y soporte conversacional. "
            "Aún no analiza tus datos en profundidad."
        ),
        "features": [
            "Carga inventario y ventas con plantillas validadas",
            "Smart Importer con mapeo automático de columnas",
            "Concierge IA que te guía paso a paso",
            "Soporte por email + tickets",
        ],
        "ai_capabilities": [
            "Onboarding conversacional",
            "Resolver dudas sobre cómo usar la plataforma",
            "Sugerir el siguiente paso del flujo",
        ],
        "limits": {
            "ai_messages_per_day": 50,
            "skus": 2_000,
            "ai_can_analyze": False,
            "ai_can_act": False,
        },
    },
    "pro": {
        "name": "Pro",
        "tagline": "El Analista de Inventarios",
        "price_monthly_usd": 40,
        "ai_persona": "analyst",
        "ai_persona_label": "Analista de Inventarios",
        "summary": (
            "Análisis ABC/XYZ con explicación del por qué de cada decisión. "
            "Stock de seguridad y ROP justificados con lenguaje ejecutivo."
        ),
        "features": [
            "Todo lo de Starter",
            "Análisis ABC/XYZ con narrativa explicada por la IA",
            "Stock de seguridad y punto de reorden razonados",
            "Chat sobre el porqué de cada sugerencia",
            "Snapshots persistentes de inventario y ventas",
        ],
        "ai_capabilities": [
            "Lee snapshots reales del tenant",
            "Explica clasificación ABC/XYZ con lenguaje ejecutivo",
            "Justifica ROP, SS y sugerencia de compra por SKU",
            "Conversación con memoria por tenant",
        ],
        "limits": {
            "ai_messages_per_day": 300,
            "skus": 25_000,
            "ai_can_analyze": True,
            "ai_can_act": False,
        },
    },
    "enterprise": {
        "name": "Enterprise",
        "tagline": "El Director de Operaciones (COO)",
        "price_monthly_usd": 100,
        "ai_persona": "coo",
        "ai_persona_label": "COO Autónomo",
        "summary": (
            "Toma acciones reales: genera órdenes de compra listas para firma, "
            "exporta Excel/PDF y prepara correos de reposición."
        ),
        "features": [
            "Todo lo de Pro",
            "IA con function calling: genera Excel y PDF",
            "Órdenes de compra editables y persistentes",
            "Correos de reposición listos para enviar",
            "SKUs y usuarios ilimitados",
            "Soporte prioritario",
        ],
        "ai_capabilities": [
            "Function calling: genera órdenes, exporta Excel, redacta correos",
            "Persistencia tenant-scoped de cada acción",
            "Audit log con cada decisión ejecutada",
        ],
        "limits": {
            "ai_messages_per_day": 1_500,
            "skus": None,  # ilimitado
            "ai_can_analyze": True,
            "ai_can_act": True,
        },
    },
}


# Feature keys consumidos por core.access.feature_enabled.
# Cualquier vista/servicio que necesite control de acceso debe usar estas
# claves en lugar de comparar strings de plan a mano.
FEATURE_REQUIREMENTS: dict[str, str] = {
    "ai_chat": "starter",
    "ai_analysis": "pro",
    "ai_function_calling": "enterprise",
    "purchase_orders_editable": "pro",
    "purchase_orders_export": "enterprise",
    "purchase_orders_email": "enterprise",
    "snapshots_persisted": "pro",
    "advanced_dashboard": "pro",
    "white_label_branding": "enterprise",
}


def normalize_plan(plan: str | None) -> str:
    if not plan:
        return "free"
    plan = plan.lower().strip()
    if plan not in PLAN_RANK:
        return "free"
    return plan


def plan_rank(plan: str | None) -> int:
    return PLAN_RANK.get(normalize_plan(plan), 0)


def has_minimum_plan(current: str | None, required: str) -> bool:
    return plan_rank(current) >= plan_rank(required)


def feature_enabled(plan: str | None, feature_key: str) -> bool:
    required = FEATURE_REQUIREMENTS.get(feature_key)
    if required is None:
        return True
    return has_minimum_plan(plan, required)


def plan_info(plan_key: str) -> dict | None:
    return PLAN_CATALOG.get(normalize_plan(plan_key))


def public_catalog() -> Iterable[tuple[str, dict]]:
    """Itera el catálogo en el orden comercial deseado."""
    for key in PLAN_KEYS:
        yield key, PLAN_CATALOG[key]
