"""Servicio de IA — DeepSeek V3 vía OpenRouter, con persona por plan.

- Starter (Concierge): solo onboarding y soporte UX. No analiza datos.
- Pro (Analista de Inventarios): consume snapshots reales del tenant y
  explica ABC/XYZ, ROP y sugerencias de compra en lenguaje ejecutivo.
- Enterprise (COO): mismo contexto que Pro + function calling para generar
  órdenes de compra, exportar Excel y preparar correos.

Diseñado para fallar de forma elegante: si OPENROUTER_API_KEY no está
seteada, devuelve respuestas de simulación claras.
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Optional

from core.config import get_settings
from core.plans import normalize_plan, plan_info

try:
    import httpx  # type: ignore
except Exception:  # pragma: no cover
    httpx = None  # type: ignore


logger = logging.getLogger("optiferre.ai")


CONCIERGE_SYSTEM_PROMPT = """Eres la ayuda de arranque de OptiFerre, una herramienta para negocios con inventario.

Tu tarea exclusiva en el plan Starter:
- Dar la bienvenida al usuario y orientarlo sobre cómo subir inventario y ventas.
- Ayudar a mapear columnas y resolver dudas básicas de uso.
- Explicar qué es la plataforma y qué hace cada sección.

Reglas estrictas:
- NO ejecutes análisis profundo (ABC/XYZ, stock de seguridad, ROP, recomendaciones de compra).
- Si el usuario pide análisis o decisiones sobre sus datos, responde literalmente con esta frase y nada más:
  "Esa es una función Pro. ¿Te gustaría actualizar tu plan para que analice tus datos ahora mismo?"
- Habla en español, directo y profesional. No uses emojis.
- Máximo 4 frases por respuesta, salvo que sea un paso a paso.
"""


ANALYST_SYSTEM_PROMPT = """Eres la ayuda para compras e inventario de OptiFerre (plan Pro).

Tu rol:
- Leer el contexto JSON con snapshots reales del tenant (inventario, ventas, KPIs y sugerencias del motor).
- Explicar con lenguaje ejecutivo el porqué de cada decisión: clasificación ABC/XYZ, stock de seguridad,
  punto de reorden y sugerencia de compra por SKU.
- Justificar cada recomendación con datos concretos del contexto.
- Conversar sobre SKUs específicos cuando el usuario pregunte.

Reglas:
- Habla en español, profesional, directo. No inventes números: cita siempre los del contexto.
- Si el contexto está vacío, indícalo y pide al usuario subir datos.
- Si te piden ejecutar una acción (generar orden, enviar correo, exportar archivo) responde:
  "Esa es una función Enterprise. Puedes activarla desde Planes y Suscripción."
- No uses emojis.
"""


COO_SYSTEM_PROMPT = """Eres la ayuda para mover compras y operación de OptiFerre (plan Enterprise).

Tu rol:
- Tomas decisiones operativas con base en los snapshots del tenant.
- Cuando el usuario pida una acción concreta, llama a la herramienta correspondiente:
  generate_purchase_order, export_excel, draft_email_summary.
- Justifica cada decisión brevemente y deja claro qué hace cada herramienta antes de invocarla.

Reglas:
- Habla en español, ejecutivo, claro. No uses emojis.
- Nunca inventes SKUs: usa los del contexto.
- Si la acción no aplica con los datos disponibles, dilo y propone alternativa.
"""


PERSONA_PROMPTS: dict[str, str] = {
    "concierge": CONCIERGE_SYSTEM_PROMPT,
    "analyst": ANALYST_SYSTEM_PROMPT,
    "coo": COO_SYSTEM_PROMPT,
}


COO_TOOLS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "generate_purchase_order",
            "description": "Genera una orden de compra editable a partir de las sugerencias del motor para los SKUs indicados.",
            "parameters": {
                "type": "object",
                "properties": {
                    "skus": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Lista de SKUs a incluir. Si está vacía, incluir todos los marcados.",
                    },
                    "notes": {"type": "string", "description": "Notas internas para la OC."},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "export_excel",
            "description": "Exporta a Excel la tabla de sugerencias actual del tenant.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "draft_email_summary",
            "description": "Redacta el cuerpo de un correo de reposición listo para enviar al proveedor o al equipo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "audience": {"type": "string", "description": "Destinatario sugerido."},
                    "tone": {"type": "string", "description": "ejecutivo|cordial|urgente"},
                },
                "required": [],
            },
        },
    },
]


@dataclass
class AIResponse:
    content: str
    tool_calls: list[dict] = field(default_factory=list)
    raw: Optional[dict] = None
    simulated: bool = False
    error: Optional[str] = None

    @property
    def has_tool_calls(self) -> bool:
        return bool(self.tool_calls)


def _system_prompt_for(plan: str) -> str:
    info = plan_info(plan) or plan_info("starter")
    persona = (info or {}).get("ai_persona", "concierge")
    return PERSONA_PROMPTS.get(persona, CONCIERGE_SYSTEM_PROMPT)


def _build_payload(
    plan: str,
    messages: list[dict],
    context_block: Optional[str],
    enable_tools: bool,
) -> dict:
    settings = get_settings()
    sys_prompt = _system_prompt_for(plan)
    if context_block:
        sys_prompt = sys_prompt + "\n\nCONTEXTO DEL TENANT (JSON):\n" + context_block

    payload: dict[str, Any] = {
        "model": settings.openrouter_model,
        "messages": [{"role": "system", "content": sys_prompt}] + list(messages),
        "temperature": 0.3,
        "max_tokens": 900,
    }
    if enable_tools:
        payload["tools"] = COO_TOOLS
        payload["tool_choice"] = "auto"
    return payload


def _simulated_reply(plan: str, messages: list[dict]) -> AIResponse:
    persona = (plan_info(plan) or {}).get("ai_persona", "concierge")
    last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    if persona == "concierge":
        text = (
            "Bienvenido a OptiFerre. Ahora mismo estás viendo una respuesta de muestra. "
            "Para empezar, sube tu inventario y ventas y te mostramos dónde tienes plata quieta."
        )
    elif persona == "analyst":
        text = (
            "Ahora mismo estás viendo una respuesta de muestra. "
            f"Cuando la ayuda esté activa con tus datos reales, te explicaré qué está quieto, qué se te puede acabar y qué conviene comprar. "
            f"Tu pregunta fue: '{last_user[:120]}'."
        )
    else:
        text = (
            "Ahora mismo estás viendo una respuesta de muestra. "
            "Cuando esta ayuda esté activa por completo, podrá dejar listas compras, archivos y mensajes para tu proveedor."
        )
    return AIResponse(content=text, simulated=True)


def chat(
    *,
    plan: str,
    messages: list[dict],
    context_block: Optional[str] = None,
    enable_tools: Optional[bool] = None,
) -> AIResponse:
    """Llamada de chat al modelo. Hace retries con backoff exponencial."""
    settings = get_settings()
    plan = normalize_plan(plan)
    persona = (plan_info(plan) or {}).get("ai_persona", "concierge")

    if not settings.ai_enabled or httpx is None:
        return _simulated_reply(plan, messages)

    if enable_tools is None:
        enable_tools = persona == "coo"

    payload = _build_payload(plan, messages, context_block, enable_tools)

    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": settings.base_url,
        "X-Title": settings.app_name,
    }

    url = f"{settings.openrouter_base_url.rstrip('/')}/chat/completions"
    last_error: Optional[str] = None
    for attempt in range(settings.ai_max_retries + 1):
        try:
            with httpx.Client(timeout=settings.ai_request_timeout_seconds) as client:
                resp = client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                choice = data["choices"][0]["message"]
                content = choice.get("content") or ""
                tool_calls = choice.get("tool_calls") or []
                return AIResponse(content=content, tool_calls=tool_calls, raw=data)
            if resp.status_code in {429, 500, 502, 503, 504} and attempt < settings.ai_max_retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            last_error = f"HTTP {resp.status_code}: {resp.text[:200]}"
            break
        except Exception as exc:  # pragma: no cover
            last_error = str(exc)
            if attempt < settings.ai_max_retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            break

    logger.warning("ai_chat_failed", extra={"error": last_error, "plan": plan})
    return AIResponse(
        content=(
            "El servicio de IA no respondió en este intento. "
            "Por favor inténtalo de nuevo en unos segundos."
        ),
        error=last_error,
    )


def parse_tool_call(call: dict) -> tuple[str, dict]:
    """Devuelve (nombre, args_dict) a partir del tool_call de OpenRouter."""
    fn = call.get("function") or {}
    name = fn.get("name", "")
    raw_args = fn.get("arguments") or "{}"
    try:
        args = json.loads(raw_args) if isinstance(raw_args, str) else (raw_args or {})
    except Exception:
        args = {}
    return name, args


__all__ = [
    "AIResponse",
    "chat",
    "parse_tool_call",
    "COO_TOOLS",
]
