from fastapi import APIRouter, HTTPException

from app.services.brasil_api import buscar_cep
from app.services.cache import get_or_fetch

router = APIRouter(prefix="/api/cep", tags=["CEP"])


@router.get("/{cep}")
async def get_cep(cep: str):
    digits = "".join(c for c in cep if c.isdigit())
    if len(digits) != 8:
        raise HTTPException(400, "CEP deve ter 8 dígitos")
    data = await get_or_fetch(f"cep:{digits}", lambda: buscar_cep(digits))
    if not data:
        raise HTTPException(404, "CEP não encontrado")
    return data
