# Cadastro API

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white">
  <img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white">
  <img src="https://img.shields.io/badge/HTTPX-000000?style=for-the-badge">
  <img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white">
  <img src="https://img.shields.io/badge/JWT-HS256-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white">
  <img src="https://img.shields.io/badge/License-MIT-success?style=for-the-badge">
</p>

<p align="center">
REST API para gerenciamento de clientes (Pessoa Física e Jurídica) desenvolvida com FastAPI, PostgreSQL e Redis.
<br>
Integra a BrasilAPI para preenchimento automático de dados e utiliza cache para reduzir latência e chamadas externas.
</p>

# Tecnologias

| Backend        | Banco      | Infra | Testes |
| -------------- | ---------- | ----- | ------ |
| FastAPI        | PostgreSQL | Redis | Pytest |
| SQLAlchemy 2.0 | AsyncPG    | HTTPX |        |
| Pydantic v2    |            | JWT   |        |

---

# Arquitetura

```text
                 Cliente

      Browser / Mobile / Postman
                   │
                   ▼
              FastAPI REST API
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
 PostgreSQL      Redis     BrasilAPI
 Persistência     Cache     APIs Externas
```

---

# Funcionalidades

* CRUD completo de clientes (Pessoa Física e Jurídica)
* Consulta automática de endereço por CEP
* Consulta automática de empresas por CNPJ
* Cache Redis com TTL de 30 dias
* Validação de CPF
* Validação de CNPJ
* Autenticação JWT
* Paginação
* Filtros dinâmicos
* Geolocalização utilizando Haversine
* Documentação automática via Swagger e ReDoc

---

# Endpoints

| Método | Endpoint             | Descrição         | Auth |
| ------ | -------------------- | ----------------- | ---- |
| POST   | `/api/auth/token`    | Gerar Token JWT   | ❌    |
| GET    | `/api/cep/{cep}`     | Buscar endereço   | ❌    |
| GET    | `/api/cnpj/{cnpj}`   | Buscar empresa    | ❌    |
| POST   | `/api/clientes`      | Criar cliente     | ✅    |
| GET    | `/api/clientes`      | Listar clientes   | ✅    |
| GET    | `/api/clientes/{id}` | Buscar cliente    | ✅    |
| PATCH  | `/api/clientes/{id}` | Atualizar cliente | ✅    |
| DELETE | `/api/clientes/{id}` | Remover cliente   | ✅    |
| GET    | `/`                  | Health Check      | ❌    |

---

# Estrutura do Projeto

```text
cadastro-api/
│
├── app/
│   ├── config.py
│   ├── database.py
│   ├── redis_client.py
│   ├── auth.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── cep.py
│   │   ├── cnpj.py
│   │   └── clientes.py
│   │
│   └── services/
│       ├── brasil_api.py
│       └── cache.py
│
├── tests/
│
├── schema.sql
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

---

# Instalação

## 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/cadastro-api.git

cd cadastro-api
```

## 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 4. Crie o banco

```bash
psql -U postgres -c "CREATE DATABASE cadastro_db;"
```

## 5. Execute o schema

```bash
psql -U postgres -d cadastro_db -f schema.sql
```

## 6. Configure o ambiente

```bash
cp .env.example .env
```

---

# Variáveis de Ambiente

```env
DATABASE_URL=postgresql+asyncpg://postgres:senha@localhost/cadastro_db

REDIS_URL=redis://localhost:6379/0

JWT_SECRET_KEY=sua_chave_super_secreta
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

BRASIL_API_URL=https://brasilapi.com.br/api

DEBUG=True
```

---

# Executando

```bash
uvicorn app.main:app --reload
```

Aplicação disponível em:

| Serviço | URL                         |
| ------- | --------------------------- |
| API     | http://localhost:8000       |
| Swagger | http://localhost:8000/docs  |
| ReDoc   | http://localhost:8000/redoc |

---

# Exemplos

## Gerar Token

```bash
curl -X POST http://localhost:8000/api/auth/token \
-H "Content-Type: application/json" \
-d '{
"username":"admin",
"password":"admin"
}'
```

## Criar Cliente

```bash
curl -X POST http://localhost:8000/api/clientes \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{
"tipo":"PF",
"cpf_cnpj":"12345678901",
"nome_razao_social":"João da Silva",
"cep":"01001000",
"numero":"100"
}'
```

---

# Testes

Execute:

```bash
pytest -v
```

Cobertura:

* Autenticação
* CRUD
* CPF
* CNPJ
* CEP
* Paginação
* Filtros
* Health Check

---

# Banco de Dados

### Tabelas

* clientes
* campos_pj (1:1)

### Índices

* CPF/CNPJ
* Estado
* Cidade
* Tipo
* GIN Trigram

---

# Decisões Técnicas

* SQLAlchemy 2.0 Async para I/O não bloqueante.
* HTTPX Async para chamadas externas.
* Redis reduz chamadas repetidas à BrasilAPI.
* JWT Stateless.
* Pydantic v2 para validação.
* Cache de CEP e CNPJ com TTL de 30 dias.
* Arquitetura organizada em camadas (`routes`, `services`, `models`, `schemas`).

---

# Roadmap

* [x] CRUD de clientes
* [x] BrasilAPI
* [x] Redis
* [x] JWT
* [x] Validação CPF/CNPJ
* [x] Paginação
* [x] Filtros
* [x] Testes automatizados
* [ ] Docker
* [ ] Docker Compose
* [ ] Alembic
* [ ] GitHub Actions
* [ ] Deploy
* [ ] Rate Limiting
* [ ] Observabilidade

---

# Licença

Distribuído sob a licença **MIT**.
