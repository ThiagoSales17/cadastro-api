import re
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r"\D", "", cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        s = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        d = (s * 10) % 11
        if d == 10:
            d = 0
        if int(cpf[i]) != d:
            return False
    return True


def _validar_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r"\D", "", cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1
    for i, pesos in enumerate([pesos1, pesos2]):
        s = sum(int(cnpj[j]) * pesos[j] for j in range(len(pesos)))
        d = s % 11
        d = 0 if d < 2 else 11 - d
        if int(cnpj[12 + i]) != d:
            return False
    return True


def validar_cpf_cnpj(v: str | None) -> str | None:
    if v is None:
        return v
    digits = re.sub(r"\D", "", v)
    if len(digits) == 11:
        if not _validar_cpf(digits):
            raise ValueError("CPF inválido")
    elif len(digits) == 14:
        if not _validar_cnpj(digits):
            raise ValueError("CNPJ inválido")
    else:
        raise ValueError("CPF/CNPJ deve ter 11 ou 14 dígitos")
    return digits


class ClienteBase(BaseModel):
    cpf_cnpj: str
    nome_razao_social: str = Field(..., min_length=2, max_length=255)
    email: str | None = None
    telefone: str | None = None
    cep: str | None = None
    rua: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None

    _validar_cpf_cnpj = field_validator("cpf_cnpj")(validar_cpf_cnpj)


class ClienteCreate(ClienteBase):
    tipo: str = Field(..., pattern="^(PF|PJ)$")


class ClientePJExtra(BaseModel):
    nome_fantasia: str | None = None
    cnae_principal: str | None = None
    cnae_descricao: str | None = None
    capital_social: float | None = None
    natureza_juridica: str | None = None
    porte: str | None = None
    situacao_cadastral: str | None = None
    data_abertura: date | None = None


class ClienteCreatePJ(ClienteCreate):
    campos_pj: ClientePJExtra | None = None


class ClienteUpdate(BaseModel):
    nome_razao_social: str | None = None
    email: str | None = None
    telefone: str | None = None
    cep: str | None = None
    rua: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None


class ClienteResponse(ClienteBase):
    id: int
    tipo: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClientePJResponse(ClienteResponse):
    campos_pj: ClientePJExtra | None = None
