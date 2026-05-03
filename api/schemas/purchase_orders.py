from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PurchaseOrderCreateRequest(BaseModel):
    only_skus: Optional[list[str]] = None
    notes: Optional[str] = None


class PurchaseOrderResponse(BaseModel):
    id: int
    code: str
    status: str
    total_units: float
    total_amount: float
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None


class PurchaseOrderCreateResponse(BaseModel):
    ok: bool
    id: Optional[int] = None
    code: Optional[str] = None
    items: int = 0
    total_units: float = 0
    total_amount: float = 0
    reason: Optional[str] = None
