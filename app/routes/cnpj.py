from fastapi import APIRouter, HTTPException

from app.services.brasil_api import buscar_cnpj
from app.services.cache import get_or_fetch

router = APIRouter(prefix="/api/cnpj", tags=["CNPJ"])


@router.get("/{cnpj}")
async def get_cnpj(cnpj: str):
    digits = "".join(c for c in cnpj if c.isdigit())
    if len(digits) != 14:
        raise HTTPException(400, "CNPJ deve ter 14 dígitos")
    data = await get_or_fetch(f"cnpj:{digits}", lambda: buscar_cnpj(digits))
    if not data:
        raise HTTPException(404, "CNPJ não encontrado")
    return data
