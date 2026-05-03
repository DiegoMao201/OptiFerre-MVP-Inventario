"""Plantillas oficiales para onboarding de carga."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response

from core.templates import ALL_TEMPLATES, iter_templates

router = APIRouter()


@router.get("")
def list_templates() -> dict:
    return {
        "items": [
            {
                "key": template.key,
                "title": template.title,
                "description": template.description,
                "required_columns": list(template.required_columns),
                "sample_rows": template.sample_rows,
                "csv_url": f"/templates/{template.key}.csv",
                "xlsx_url": f"/templates/{template.key}.xlsx",
            }
            for template in iter_templates()
        ]
    }


@router.get("/{template_key}.{fmt}")
def download_template(template_key: str, fmt: str) -> Response:
    template = ALL_TEMPLATES.get(template_key)
    if not template:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada.")

    if fmt == "csv":
        return Response(
            content=template.to_csv_bytes(),
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="plantilla_{template_key}.csv"'},
        )
    if fmt == "xlsx":
        return Response(
            content=template.to_xlsx_bytes(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="plantilla_{template_key}.xlsx"'},
        )

    raise HTTPException(status_code=400, detail="Formato no soportado.")