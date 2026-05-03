"""Órdenes de Compra: tabla editable + persistencia + exportación."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from core.access import can, require_feature
from core.auth import require_login
from services.inventory_store import (
    apply_suggestion_edits,
    list_suggestions,
    upsert_suggestions_from_analysis,
)
from services.purchase_orders import (
    create_purchase_order_from_suggestions,
    export_order_excel,
    list_orders,
)
from ui.components import format_currency, paywall_card, section_shell


def _refresh_from_analysis(user: dict) -> int:
    df = st.session_state.get("analysis_result")
    if df is None or df.empty:
        return 0
    return upsert_suggestions_from_analysis(
        user["tenant_id"], df, updated_by=user["email"]
    )


def render() -> None:
    user = require_login()
    if not require_feature(
        "purchase_orders_editable",
        user=user,
        title="Órdenes de Compra editables — Plan Pro",
        description=(
            "Tu equipo necesita el plan <b>Pro</b> para editar, ajustar y persistir las sugerencias "
            "de compra de la IA."
        ),
    ):
        return

    section_shell(
        "Órdenes de Compra",
        "Edita las cantidades sugeridas por la IA, marca lo que entra al pedido y genera la orden persistente.",
        eyebrow="Decisión accionable",
    )

    cols = st.columns([1, 1, 4])
    if cols[0].button("🔄 Sincronizar con análisis", use_container_width=True):
        added = _refresh_from_analysis(user)
        st.success(f"{added} SKUs sincronizados desde el último análisis.")

    suggestions = list_suggestions(user["tenant_id"])
    if not suggestions:
        st.info(
            "Aún no hay sugerencias persistidas. Ejecuta el análisis en Dashboard "
            "y vuelve a sincronizar aquí."
        )
        return

    df = pd.DataFrame(suggestions)
    df["qty_user"] = df["qty_user"].fillna(df["qty_ai"])
    df["valor_linea"] = df["qty_user"].astype(float) * df["unit_cost"].astype(float)

    edited = st.data_editor(
        df[
            [
                "sku",
                "name",
                "qty_ai",
                "qty_user",
                "unit_cost",
                "valor_linea",
                "included",
                "notes",
            ]
        ],
        use_container_width=True,
        hide_index=True,
        column_config={
            "sku": st.column_config.TextColumn("SKU", disabled=True),
            "name": st.column_config.TextColumn("Nombre", disabled=True),
            "qty_ai": st.column_config.NumberColumn("Sugerido IA", disabled=True),
            "qty_user": st.column_config.NumberColumn("Cantidad final", min_value=0),
            "unit_cost": st.column_config.NumberColumn("Costo unit.", disabled=True, format="$ %.2f"),
            "valor_linea": st.column_config.NumberColumn("Total línea", disabled=True, format="$ %.2f"),
            "included": st.column_config.CheckboxColumn("Incluir en OC"),
            "notes": st.column_config.TextColumn("Notas"),
        },
        num_rows="fixed",
        key="po_editor",
    )

    total_units = float(edited[edited["included"]]["qty_user"].sum())
    total_amount = float((edited[edited["included"]]["qty_user"] * edited[edited["included"]]["unit_cost"]).sum())

    kpi_cols = st.columns(3)
    kpi_cols[0].metric("Líneas seleccionadas", int(edited["included"].sum()))
    kpi_cols[1].metric("Unidades totales", f"{total_units:,.0f}")
    kpi_cols[2].metric("Monto estimado", format_currency(total_amount))

    if st.button("💾 Guardar cambios", use_container_width=True):
        apply_suggestion_edits(
            user["tenant_id"],
            edited.to_dict(orient="records"),
            updated_by=user["email"],
        )
        st.success("Cambios guardados.")
        st.rerun()

    st.divider()

    can_export = can(user, "purchase_orders_export")
    if not can_export:
        paywall_card(
            current_plan="pro",
            required_plan="enterprise",
            feature_key="purchase_orders_export",
            title="La generación de OC y exportación a Excel es Enterprise",
            description=(
                "Tu plan Pro te permite editar y persistir las sugerencias. "
                "Activa <b>Enterprise</b> para generar la orden, exportarla a Excel y "
                "preparar correos automáticos."
            ),
        )
    else:
        col1, col2 = st.columns(2)
        if col1.button("🧾 Generar Orden de Compra", use_container_width=True, type="primary"):
            apply_suggestion_edits(
                user["tenant_id"],
                edited.to_dict(orient="records"),
                updated_by=user["email"],
            )
            result = create_purchase_order_from_suggestions(
                user["tenant_id"], created_by=user["email"]
            )
            if result.get("ok"):
                st.session_state["_last_po_id"] = result["id"]
                st.success(
                    f"OC {result['code']} creada · {result['items']} líneas · "
                    f"{format_currency(result['total_amount'])}"
                )
            else:
                st.warning("No hay líneas marcadas para incluir.")
        last_id = st.session_state.get("_last_po_id")
        if last_id:
            data = export_order_excel(user["tenant_id"], last_id)
            if data:
                col2.download_button(
                    "⬇️ Descargar última OC (Excel)",
                    data,
                    file_name=f"orden_compra_{last_id}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

    st.markdown("### 📚 Historial de órdenes")
    orders = list_orders(user["tenant_id"])
    if not orders:
        st.caption("Aún no se han generado órdenes.")
    else:
        st.dataframe(
            pd.DataFrame(orders),
            use_container_width=True,
            hide_index=True,
        )
