from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import get_current_user
from app.database import get_session
from app.models import Cliente, CamposPJ
from app.schemas import (
    ClienteCreatePJ,
    ClienteResponse,
    ClientePJResponse,
    ClienteUpdate,
)

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def criar_cliente(
    data: ClienteCreatePJ,
    session: AsyncSession = Depends(get_session),
    _: str = Depends(get_current_user),
):
    existing = await session.execute(
        select(Cliente).where(
            (Cliente.cpf_cnpj == data.cpf_cnpj) | (Cliente.email == data.email)
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(409, "CPF/CNPJ ou email já cadastrado")

    cliente = Cliente(
        tipo=data.tipo,
        cpf_cnpj=data.cpf_cnpj,
        nome_razao_social=data.nome_razao_social,
        email=data.email,
        telefone=data.telefone,
        cep=data.cep,
        rua=data.rua,
        numero=data.numero,
        complemento=data.complemento,
        bairro=data.bairro,
        cidade=data.cidade,
        estado=data.estado,
    )
    session.add(cliente)
    await session.flush()

    if data.tipo == "PJ" and data.campos_pj:
        campos = CamposPJ(
            cliente_id=cliente.id,
            nome_fantasia=data.campos_pj.nome_fantasia,
            cnae_principal=data.campos_pj.cnae_principal,
            cnae_descricao=data.campos_pj.cnae_descricao,
            capital_social=data.campos_pj.capital_social,
            natureza_juridica=data.campos_pj.natureza_juridica,
            porte=data.campos_pj.porte,
            situacao_cadastral=data.campos_pj.situacao_cadastral,
            data_abertura=data.campos_pj.data_abertura,
        )
        session.add(campos)

    await session.commit()
    await session.refresh(cliente)
    return Response(
        content=ClienteResponse.model_validate(cliente).model_dump_json(),
        media_type="application/json",
        status_code=201,
        headers={"Location": f"/api/clientes/{cliente.id}"},
    )


@router.get("/", response_model=list[ClienteResponse])
async def listar_clientes(
    session: AsyncSession = Depends(get_session),
    _: str = Depends(get_current_user),
    nome: str | None = Query(None, min_length=2),
    cpf_cnpj: str | None = Query(None),
    cidade: str | None = Query(None, min_length=2),
    estado: str | None = Query(None, max_length=2),
    tipo: str | None = Query(None, pattern="^(PF|PJ)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    query = select(Cliente)
    if nome:
        query = query.where(Cliente.nome_razao_social.ilike(f"%{nome}%"))
    if cpf_cnpj:
        query = query.where(Cliente.cpf_cnpj == cpf_cnpj)
    if cidade:
        query = query.where(Cliente.cidade.ilike(f"%{cidade}%"))
    if estado:
        query = query.where(Cliente.estado == estado.upper())
    if tipo:
        query = query.where(Cliente.tipo == tipo)
    result = await session.execute(query.order_by(Cliente.id).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{cliente_id}", response_model=ClientePJResponse)
async def buscar_cliente(
    cliente_id: int,
    session: AsyncSession = Depends(get_session),
    _: str = Depends(get_current_user),
):
    result = await session.execute(
        select(Cliente).where(Cliente.id == cliente_id).options(selectinload(Cliente.campos_pj))
    )
    cliente = result.scalar_one_or_none()
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")
    return cliente


@router.patch("/{cliente_id}", response_model=ClienteResponse)
async def atualizar_cliente(
    cliente_id: int,
    data: ClienteUpdate,
    session: AsyncSession = Depends(get_session),
    _: str = Depends(get_current_user),
):
    result = await session.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente = result.scalar_one_or_none()
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(cliente, campo, valor)

    await session.commit()
    await session.refresh(cliente)
    return cliente


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_cliente(
    cliente_id: int,
    session: AsyncSession = Depends(get_session),
    _: str = Depends(get_current_user),
):
    result = await session.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente = result.scalar_one_or_none()
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")

    await session.delete(cliente)
    await session.commit()
    return Response(status_code=204)
