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
        "tagline": "Empieza bien sin enredarte",
        "price_monthly_usd": 15,
        "ai_persona": "concierge",
        "ai_persona_label": "Concierge Onboarding",
        "summary": (
            "Te ordena la entrada de datos, te evita errores de carga y te acompaña "
            "para que en pocos minutos puedas ver el negocio sin fricción."
        ),
        "sales_pitch": (
            "Para el cliente que hoy sigue peleando con archivos sueltos, columnas mal puestas "
            "y tiempo perdido antes de poder decidir algo útil."
        ),
        "upgrade_trigger": (
            "Cuando ya lograste subir bien la información y quieres saber qué producto te está "
            "dejando plata quieta, el siguiente paso natural es Pro."
        ),
        "cta_label": "Quiero ordenar mi operación",
        "features": [
            "Carga inventario y ventas con plantillas claras",
            "Te guiamos para dejar los archivos listos sin ensayo y error",
            "Acompañamiento por tickets y onboarding guiado",
            "Base lista para crecer sin volver a empezar",
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
        "tagline": "Decide qué comprar y qué dejar de mover",
        "price_monthly_usd": 40,
        "ai_persona": "analyst",
        "ai_persona_label": "Analista de Inventarios",
        "summary": (
            "Te muestra en pesos qué tienes quieto, qué se te va a acabar y cuánto deberías "
            "comprar para vender mejor sin inflar la bodega."
        ),
        "sales_pitch": (
            "Para el negocio que ya no quiere mirar el inventario a punta de intuición, sino con "
            "decisiones concretas que cuiden caja, rotación y ventas."
        ),
        "upgrade_trigger": (
            "Cuando ya ves el problema y quieres que la plataforma te ayude a ejecutar órdenes, "
            "correos y acciones reales, el siguiente paso es Enterprise."
        ),
        "cta_label": "Quiero decisiones claras",
        "features": [
            "Todo lo de Starter",
            "Productos muertos, quiebres y compra sugerida con contexto",
            "Análisis explicado en lenguaje de negocio, no técnico",
            "Punto de reorden y stock sugerido con justificación",
            "Historial persistente para seguir afinando decisiones",
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
        "tagline": "Convierte análisis en ejecución real",
        "price_monthly_usd": 100,
        "ai_persona": "coo",
        "ai_persona_label": "COO Autónomo",
        "summary": (
            "Te ayuda a pasar del diagnóstico a la operación: órdenes listas, comunicación con "
            "proveedores y control para equipos con más volumen."
        ),
        "sales_pitch": (
            "Para empresas que ya no necesitan solo ver el problema, sino mover compras, equipos y "
            "proveedores con menos fricción y más control."
        ),
        "upgrade_trigger": (
            "Este es el nivel para cuando el cliente ya confía en la plataforma y quiere delegar "
            "más trabajo operativo sin perder visibilidad."
        ),
        "cta_label": "Quiero operar más rápido",
        "features": [
            "Todo lo de Pro",
            "Órdenes de compra editables y listas para trabajar",
            "Correos de reposición listos para enviar al proveedor",
            "Mayor volumen, más usuarios y menos fricción operativa",
            "Soporte prioritario para equipos que no pueden frenar",
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
