# API de Cadastro Inteligente

API REST para gerenciamento de cadastros de clientes (PF/PJ) com auto-preenchimento via BrasilAPI. Reduz fricção no registro: menos campos manuais = maior conversão.

**Stack:** Python 3.11+ · FastAPI · PostgreSQL · Redis · httpx (async)

## Features

- CRUD completo de clientes (Pessoa Física e Jurídica)
- Auto-preenchimento de endereço por CEP (BrasilAPI v2 com geolocalização)
- Auto-preenchimento de dados de empresa por CNPJ (BrasilAPI)
- Cache Redis com TTL de 30 dias para consultas externas
- Validação de CPF/CNPJ com dígitos verificadores
- Autenticação JWT (HS256, 1h de expiração, issuer validation)
- Paginação e filtros (tipo, nome, estado, cidade, CPF/CNPJ)
- Geolocalização para cálculo de distância (Haversine)

## Rotas

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| `POST` | `/api/auth/token` | Obter token JWT | — |
| `GET` | `/api/cep/{cep}` | Auto-preenche endereço por CEP | — |
| `GET` | `/api/cnpj/{cnpj}` | Auto-preenche empresa por CNPJ | — |
| `POST` | `/api/clientes` | Cria cliente PF ou PJ | JWT |
| `GET` | `/api/clientes` | Lista clientes (com filtros e paginação) | JWT |
| `GET` | `/api/clientes/{id}` | Busca cliente por ID | JWT |
| `PATCH` | `/api/clientes/{id}` | Atualiza cliente | JWT |
| `DELETE` | `/api/clientes/{id}` | Deleta cliente | JWT |
| `GET` | `/` | Health check (app + debug) | — |

## Pré-requisitos

- Python 3.11+
- PostgreSQL rodando
- Redis rodando

## Instalação

```bash
# Criar banco
psql -U postgres -c "CREATE DATABASE cadastro_db;"

# Criar tabelas
psql -U postgres -d cadastro_db -f schema.sql

# Ambiente virtual
python -m venv .venv
source .venv/bin/activate

# Dependências
pip install -r requirements.txt

# Configurar ambiente
cp .env.example .env
# Edite .env com suas credenciais
```

## Uso

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Autenticação

```bash
# Obter token
curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Usar token
curl http://localhost:8000/api/clientes/ \
  -H "Authorization: Bearer <token>"
```

### Criar cliente PF

```bash
curl -X POST http://localhost:8000/api/clientes \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "PF",
    "cpf_cnpj": "12345678901",
    "nome_razao_social": "João da Silva",
    "email": "joao@email.com",
    "cep": "01001000",
    "rua": "Praça da Sé",
    "numero": "100",
    "bairro": "Sé",
    "cidade": "São Paulo",
    "estado": "SP"
  }'
```

## Estrutura

```
cadastro-api/
├── app/
│   ├── main.py              # FastAPI app, CORS, lifespan
│   ├── config.py            # Settings via pydantic-settings
│   ├── database.py          # Conexão PostgreSQL (asyncpg)
│   ├── redis_client.py      # Conexão Redis
│   ├── auth.py              # JWT create/decode
│   ├── models.py            # SQLAlchemy 2.0 ORM
│   ├── schemas.py           # Pydantic V2 schemas + CPF/CNPJ validator
│   ├── routes/
│   │   ├── auth.py          # POST /api/auth/token
│   │   ├── cep.py           # GET /api/cep/{cep}
│   │   ├── cnpj.py          # GET /api/cnpj/{cnpj}
│   │   └── clientes.py      # CRUD /api/clientes
│   └── services/
│       ├── brasil_api.py    # Client httpx async para BrasilAPI
│       └── cache.py         # Cache Redis (get/set/get_or_fetch)
├── tests/
│   └── test_api.py          # 18 testes integrados
├── schema.sql               # DDL PostgreSQL
├── .env.example
├── requirements.txt
└── pyproject.toml
```

## Testes

```bash
pytest tests/ -v
```

18 testes cobrindo: autenticação, CRUD PF/PJ, validação de CPF/CNPJ inválidos, filtros, paginação, health check.

## Banco

Schema principal (`clientes` + `campos_pj` em 1:1) com índices GIN trigram para busca textual em nome e cidade, mais índices em estado, tipo e cache expiry.

## Licença

MIT
