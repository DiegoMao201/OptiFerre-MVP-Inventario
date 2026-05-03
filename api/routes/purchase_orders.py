"""Órdenes de compra a partir de las sugerencias."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.deps.security import get_current_user
from api.schemas.purchase_orders import (
    PurchaseOrderCreateRequest,
    PurchaseOrderCreateResponse,
    PurchaseOrderResponse,
)
from services.purchase_orders import (
    create_purchase_order_from_suggestions,
    export_order_excel,
    list_orders,
)

router = APIRouter()


@router.get("", response_model=list[PurchaseOrderResponse])
def list_purchase_orders(
    limit: int = 25,
    current_user: dict = Depends(get_current_user),
) -> list[PurchaseOrderResponse]:
    rows = list_orders(current_user["tenant_id"], limit=limit)
    return [PurchaseOrderResponse(**row) for row in rows]


@router.post("/generate", response_model=PurchaseOrderCreateResponse)
def generate_purchase_order(
    payload: PurchaseOrderCreateRequest,
    current_user: dict = Depends(get_current_user),
) -> PurchaseOrderCreateResponse:
    out = create_purchase_order_from_suggestions(
        current_user["tenant_id"],
        only_skus=payload.only_skus,
        notes=payload.notes,
        created_by=current_user["email"],
    )
    return PurchaseOrderCreateResponse(**out)


@router.get("/{order_id}/export.xlsx")
def export_purchase_order(
    order_id: int,
    current_user: dict = Depends(get_current_user),
) -> Response:
    blob = export_order_excel(current_user["tenant_id"], order_id)
    if blob is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Orden no encontrada.")
    return Response(
        content=blob,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=OC-{order_id}.xlsx"},
    )
