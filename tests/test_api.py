import random
import time


def _make_cpf():
    rng = random.Random(time.time_ns())
    base = [rng.randint(0, 9) for _ in range(9)]
    s1 = sum((10 - i) * base[i] for i in range(9))
    d1 = 0 if s1 % 11 < 2 else 11 - s1 % 11
    s2 = sum((11 - i) * base[i] for i in range(9)) + 2 * d1
    d2 = 0 if s2 % 11 < 2 else 11 - s2 % 11
    return "".join(map(str, base)) + str(d1) + str(d2)


def _make_cnpj():
    rng = random.Random(time.time_ns())
    base = [rng.randint(0, 9) for _ in range(12)]
    w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    s1 = sum(w1[i] * base[i] for i in range(12))
    d1 = 0 if s1 % 11 < 2 else 11 - s1 % 11
    w2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    s2 = sum(w2[i] * base[i] for i in range(12)) + 2 * d1
    d2 = 0 if s2 % 11 < 2 else 11 - s2 % 11
    return "".join(map(str, base)) + str(d1) + str(d2)


class TestAuth:
    async def test_login_success(self, client):
        r = await client.post("/api/auth/token", json={"username": "admin", "password": "admin"})
        assert r.status_code == 200
        data = r.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_fail(self, client):
        r = await client.post("/api/auth/token", json={"username": "admin", "password": "wrong"})
        assert r.status_code == 401

    async def test_cliente_sem_token(self, client):
        r = await client.get("/api/clientes/")
        assert r.status_code == 401

    async def test_cliente_token_invalido(self, client):
        r = await client.get("/api/clientes/", headers={"Authorization": "Bearer invalid"})
        assert r.status_code == 401


class TestClientesCRUD:
    _ids = {}

    async def test_criar_pf(self, client, auth_headers):
        ts = time.time_ns()
        cpf = _make_cpf()
        r = await client.post(
            "/api/clientes/",
            json={
                "tipo": "PF",
                "cpf_cnpj": cpf,
                "nome_razao_social": "Maria Silva",
                "email": f"maria{ts}@test.com",
                "telefone": "11999998888",
                "cep": "01001000",
                "rua": "Praça da Sé",
                "numero": "100",
                "bairro": "Sé",
                "cidade": "São Paulo",
                "estado": "SP",
            },
            headers=auth_headers,
        )
        assert r.status_code == 201
        data = r.json()
        assert data["nome_razao_social"] == "Maria Silva"
        assert data["tipo"] == "PF"
        assert data["cpf_cnpj"] == cpf
        self._ids["pf"] = data["id"]

    async def test_criar_pj(self, client, auth_headers):
        ts = time.time_ns()
        cnpj = _make_cnpj()
        r = await client.post(
            "/api/clientes/",
            json={
                "tipo": "PJ",
                "cpf_cnpj": cnpj,
                "nome_razao_social": "Empresa Ltda",
                "email": f"contato{ts}@empresa.com",
                "campos_pj": {
                    "nome_fantasia": "Fantasia Ltda",
                    "cnae_principal": "6422100",
                    "capital_social": 100000.0,
                    "porte": "DEMAIS",
                    "situacao_cadastral": "ATIVA",
                },
            },
            headers=auth_headers,
        )
        assert r.status_code == 201
        data = r.json()
        assert data["tipo"] == "PJ"
        assert data["nome_razao_social"] == "Empresa Ltda"
        assert data["cpf_cnpj"] == cnpj
        self._ids["pj"] = data["id"]

    async def test_criar_cpf_invalido(self, client, auth_headers):
        r = await client.post(
            "/api/clientes/",
            json={
                "tipo": "PF",
                "cpf_cnpj": "11111111111",
                "nome_razao_social": "Teste",
            },
            headers=auth_headers,
        )
        assert r.status_code == 422

    async def test_criar_cnpj_invalido(self, client, auth_headers):
        r = await client.post(
            "/api/clientes/",
            json={
                "tipo": "PJ",
                "cpf_cnpj": "11111111111111",
                "nome_razao_social": "Teste",
            },
            headers=auth_headers,
        )
        assert r.status_code == 422

    async def test_listar(self, client, auth_headers):
        r = await client.get("/api/clientes/", headers=auth_headers)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    async def test_buscar_por_id(self, client, auth_headers):
        pf_id = self._ids.get("pf", 1)
        r = await client.get(f"/api/clientes/{pf_id}", headers=auth_headers)
        assert r.status_code == 200
        assert r.json()["id"] == pf_id

    async def test_atualizar(self, client, auth_headers):
        pf_id = self._ids.get("pf", 1)
        r = await client.patch(
            f"/api/clientes/{pf_id}",
            json={"telefone": "11900001111"},
            headers=auth_headers,
        )
        assert r.status_code == 200
        assert r.json()["telefone"] == "11900001111"

    async def test_deletar(self, client, auth_headers):
        pj_id = self._ids.get("pj", 2)
        r = await client.delete(f"/api/clientes/{pj_id}", headers=auth_headers)
        assert r.status_code == 204
        r2 = await client.get(f"/api/clientes/{pj_id}", headers=auth_headers)
        assert r2.status_code == 404

    async def test_404(self, client, auth_headers):
        r = await client.get("/api/clientes/99999", headers=auth_headers)
        assert r.status_code == 404


class TestFiltros:
    async def test_filtrar_por_tipo(self, client, auth_headers):
        r = await client.get("/api/clientes/?tipo=PF", headers=auth_headers)
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0
        assert all(c["tipo"] == "PF" for c in data)

    async def test_filtrar_por_nome(self, client, auth_headers):
        r = await client.get("/api/clientes/?nome=maria", headers=auth_headers)
        assert r.status_code == 200
        assert any("Maria" in c["nome_razao_social"] for c in r.json())

    async def test_filtrar_por_estado(self, client, auth_headers):
        r = await client.get("/api/clientes/?estado=SP", headers=auth_headers)
        assert r.status_code == 200

    async def test_paginacao(self, client, auth_headers):
        r = await client.get("/api/clientes/?skip=0&limit=1", headers=auth_headers)
        assert r.status_code == 200
        assert len(r.json()) <= 1


class TestRoot:
    async def test_root(self, client):
        r = await client.get("/")
        assert r.status_code == 200
        assert r.json()["app"] == "cadastro-api"
