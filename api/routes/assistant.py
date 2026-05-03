"""Asistente IA público para preguntas frecuentes y confianza comercial."""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from services.ai_factory import chat

router = APIRouter()


LANDING_CONTEXT = """
OptiFerre es una app SaaS para ferreterías, depósitos y negocios con inventario.

Promesa principal:
- detectar plata quieta en inventario
- mostrar productos muertos
- mostrar riesgo de quiebre
- recomendar cuánto comprar

Cómo se vende por planes:
- Starter: ordena archivos, guía la carga y resuelve dudas de uso
- Pro: analiza inventario y ventas del negocio, explica qué está quieto y qué comprar
- Enterprise: ayuda a ejecutar, generar órdenes y preparar correos operativos

Datos públicos de confianza disponibles:
- fundador: Diego Mauricio Garcia
- ciudad: Pereira, Colombia
- contacto email: diegomao.201@gmail.com
- contacto comercial: WhatsApp visible en landing

Caso piloto público de referencia:
- ferretería en Pereira
- 12.000.000 COP quietos
- 22 productos muertos
- mejora en compras en 2 semanas

Reglas de respuesta:
- responde como asesor comercial experto en SaaS e IA aplicada a inventarios
- español simple, directo y confiable
- máximo 5 frases
- no inventes integraciones ni features fuera del contexto
- si preguntan por análisis profundo, explica la diferencia entre Starter, Pro y Enterprise de forma comercial
""".strip()


class PublicQuestionRequest(BaseModel):
    question: str = Field(..., min_length=4, max_length=500)


@router.post("/public")
def public_answer(payload: PublicQuestionRequest) -> dict:
    response = chat(
        plan="starter",
        messages=[{"role": "user", "content": payload.question}],
        context_block=LANDING_CONTEXT,
        enable_tools=False,
    )
    return {
        "answer": response.content,
        "simulated": response.simulated,
        "error": response.error,
    }