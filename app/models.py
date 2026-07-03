import enum
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Enum, String, Numeric, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TipoCliente(str, enum.Enum):
    PF = "PF"
    PJ = "PJ"


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[TipoCliente] = mapped_column(Enum(TipoCliente, name="tipo_cliente"))
    cpf_cnpj: Mapped[str] = mapped_column(String(14), unique=True)
    nome_razao_social: Mapped[str] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    telefone: Mapped[str | None] = mapped_column(String(20))
    cep: Mapped[str | None] = mapped_column(String(8))
    rua: Mapped[str | None] = mapped_column(String(255))
    numero: Mapped[str | None] = mapped_column(String(10))
    complemento: Mapped[str | None] = mapped_column(String(100))
    bairro: Mapped[str | None] = mapped_column(String(100))
    cidade: Mapped[str | None] = mapped_column(String(100))
    estado: Mapped[str | None] = mapped_column(String(2))
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 8))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(11, 8))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    campos_pj: Mapped["CamposPJ | None"] = relationship(back_populates="cliente", uselist=False, passive_deletes=True)


class CamposPJ(Base):
    __tablename__ = "campos_pj"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id", ondelete="CASCADE"), unique=True)
    nome_fantasia: Mapped[str | None] = mapped_column(String(255))
    cnae_principal: Mapped[str | None] = mapped_column(String(7))
    cnae_descricao: Mapped[str | None] = mapped_column(String(255))
    capital_social: Mapped[Decimal | None] = mapped_column(Numeric(15, 2))
    natureza_juridica: Mapped[str | None] = mapped_column(String(255))
    porte: Mapped[str | None] = mapped_column(String(50))
    situacao_cadastral: Mapped[str | None] = mapped_column(String(50))
    data_abertura: Mapped[date | None] = mapped_column(nullable=True)

    cliente: Mapped[Cliente] = relationship(back_populates="campos_pj", passive_deletes=True)
