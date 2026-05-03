"""Asistente IA por plan: Concierge / Analista / COO."""
from __future__ import annotations

import json
from typing import Optional

import pandas as pd
import streamlit as st

from core.access import effective_plan, plan_summary, require_feature
from core.auth import require_login
from core.plans import plan_info
from services.ai_factory import chat, parse_tool_call
from services.inventory_store import log_ai_action
from services.purchase_orders import (
    create_purchase_order_from_suggestions,
    export_order_excel,
)
from ui.components import section_shell


def _persona_intro(plan: str) -> str:
    info = plan_info(plan) or {}
    persona = info.get("ai_persona", "concierge")
    if persona == "concierge":
        return (
            "Soy tu **Concierge**. Te guío para subir datos, mapear columnas y aprovechar la plataforma. "
            "Para análisis profundo necesitas el plan Pro."
        )
    if persona == "analyst":
        return (
            "Soy tu **Analista de Inventarios**. Leo tus snapshots reales y te explico el porqué de cada "
            "clasificación ABC/XYZ, ROP y sugerencia de compra."
        )
    return (
        "Soy tu **COO autónomo**. Puedo generar órdenes de compra, exportar a Excel y redactar correos "
        "de reposición listos para enviar."
    )


def _build_context_block(user: dict, plan: str) -> Optional[str]:
    """Para Pro/Enterprise: serializa snapshot + sugerencias en JSON breve."""
    info = plan_info(plan) or {}
    persona = info.get("ai_persona", "concierge")
    if persona == "concierge":
        return None
    from services.inventory_store import list_suggestions  # diferido

    suggestions = list_suggestions(user["tenant_id"])
    df = st.session_state.get("analysis_result")
    catalog_df = st.session_state.get("uploaded_catalog")
    summary: dict = {
        "tenant_company": user.get("company_name"),
        "plan": plan,
        "skus_in_suggestions": len(suggestions),
        "top_suggestions": [
            {
                "sku": s["sku"],
                "name": s["name"],
                "qty_ai": s["qty_ai"],
                "qty_user": s["qty_user"],
                "unit_cost": s["unit_cost"],
                "included": s["included"],
            }
            for s in suggestions[:25]
        ],
    }
    if isinstance(catalog_df, pd.DataFrame) and not catalog_df.empty:
        summary["catalog_context"] = {
            "rows": int(len(catalog_df)),
            "brands": sorted(catalog_df.get("marca", pd.Series(dtype=str)).dropna().astype(str).unique().tolist())[:15],
            "suppliers": sorted(catalog_df.get("proveedor", pd.Series(dtype=str)).dropna().astype(str).unique().tolist())[:15],
        }
    if isinstance(df, pd.DataFrame) and not df.empty:
        summary["kpis"] = {
            "skus": int(df["sku"].nunique()),
            "capital_total": float(df.get("valor_inventario", pd.Series([0])).sum()),
            "capital_inmovilizado": float(df.get("capital_inmovilizado", pd.Series([0])).sum()),
            "quiebres": int((df.get("estado") == "QUIEBRE").sum()),
            "reponer": int((df.get("estado") == "REPONER").sum()),
            "sobrestock": int((df.get("estado") == "SOBRESTOCK").sum()),
        }
    return json.dumps(summary, ensure_ascii=False, default=str)


def _execute_tool(name: str, args: dict, user: dict) -> dict:
    """Ejecuta una herramienta solicitada por el COO."""
    tenant_id = user["tenant_id"]
    if name == "generate_purchase_order":
        result = create_purchase_order_from_suggestions(
            tenant_id,
            only_skus=args.get("skus") or None,
            notes=args.get("notes"),
            created_by=user["email"],
        )
        log_ai_action(tenant_id, user.get("user_id"), None, name, args, "ok" if result.get("ok") else "noop")
        return result
    if name == "export_excel":
        # Crea OC borrador con todo lo marcado y exporta
        po = create_purchase_order_from_suggestions(
            tenant_id, created_by=user["email"], notes="Generado vía IA (export_excel)"
        )
        if not po.get("ok"):
            return po
        data = export_order_excel(tenant_id, po["id"])
        log_ai_action(tenant_id, user.get("user_id"), None, name, args, "ok")
        return {"ok": True, "code": po["code"], "bytes_len": len(data) if data else 0, "order_id": po["id"]}
    if name == "draft_email_summary":
        log_ai_action(tenant_id, user.get("user_id"), None, name, args, "ok")
        return {"ok": True, "draft": True, "audience": args.get("audience"), "tone": args.get("tone")}
    return {"ok": False, "reason": "unknown_tool"}


def _render_history(messages: list[dict]) -> None:
    for msg in messages:
        role = msg.get("role")
        if role not in {"user", "assistant"}:
            continue
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(msg.get("content") or "")
            if msg.get("tool_summary"):
                st.info(msg["tool_summary"])


def render() -> None:
    user = require_login()
    if not require_feature("ai_chat", user=user, title="El Asistente IA empieza desde el plan Starter"):
        return

    summary = plan_summary(user["tenant_id"])
    plan = summary["plan"]
    info = plan_info(plan) or {}

    section_shell(
        "Asistente IA",
        info.get("summary", _persona_intro(plan)),
        eyebrow=f"{summary['name']} · {summary['tagline']}",
    )

    st.markdown(_persona_intro(plan))

    inv_loaded = st.session_state.get("uploaded_inventory") is not None
    sales_loaded = st.session_state.get("uploaded_sales") is not None
    has_data = inv_loaded and sales_loaded

    if not has_data:
        st.info("💡 Aún puedo guiarte sin datos. Cuando subas inventario y ventas en **1. Carga de Datos**, mis respuestas serán específicas a tu negocio.")
    else:
        st.caption("Contexto activo: leo tus snapshots, sugerencias y catálogo para responderte con tus datos.")

    # historial en sesión por plan (no se persiste para no acoplar al schema todavía)
    history_key = f"ai_history_{plan}"
    if history_key not in st.session_state:
        st.session_state[history_key] = []
    history: list[dict] = st.session_state[history_key]

    suggested_questions = (
        [
            "¿Qué archivos me faltan para arrancar?",
            "¿Cómo descargo la plantilla de inventario?",
            "¿Qué hace el plan Pro que no hace el Starter?",
        ]
        if not has_data
        else [
            "¿Qué está drenando mi caja hoy?",
            "¿Qué SKUs debería comprar primero?",
            "¿Cuáles productos tengo en sobrestock?",
        ]
    )
    st.markdown("**Preguntas sugeridas:**")
    sq_cols = st.columns(len(suggested_questions))
    queued = st.session_state.pop("_assistant_quick_q", None)
    for i, q in enumerate(suggested_questions):
        if sq_cols[i].button(q, key=f"sq_{plan}_{i}", use_container_width=True):
            st.session_state["_assistant_quick_q"] = q
            st.rerun()

    cols = st.columns([1, 1, 6])
    with cols[0]:
        if st.button("🧹 Limpiar", use_container_width=True):
            st.session_state[history_key] = []
            st.rerun()

    _render_history(history)

    user_input = queued or st.chat_input("Escribe tu mensaje al asistente…")
    if not user_input:
        return

    history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    context_block = _build_context_block(user, plan)
    with st.chat_message("assistant"):
        with st.spinner("Pensando…"):
            response = chat(
                plan=plan,
                messages=[{"role": m["role"], "content": m["content"]} for m in history if m["role"] in {"user", "assistant"}],
                context_block=context_block,
            )
        st.markdown(response.content or "")
        tool_summary_text = None
        if response.has_tool_calls:
            tool_summary_lines = []
            for call in response.tool_calls:
                name, args = parse_tool_call(call)
                result = _execute_tool(name, args, user)
                tool_summary_lines.append(f"`{name}` → {result}")
            tool_summary_text = "Acciones ejecutadas:\n\n" + "\n".join(f"- {ln}" for ln in tool_summary_lines)
            st.info(tool_summary_text)
        if response.simulated:
            st.caption("Modo demo: configura OPENROUTER_API_KEY para activar respuestas reales.")
        elif response.error:
            st.caption(f"Error IA: {response.error}")

    history.append(
        {
            "role": "assistant",
            "content": response.content or "",
            "tool_summary": tool_summary_text,
        }
    )
