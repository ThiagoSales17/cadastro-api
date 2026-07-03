import httpx

BASE_URL = "https://brasilapi.com.br/api"
_client = httpx.AsyncClient(timeout=10)


async def buscar_cep(cep: str) -> dict:
    response = await _client.get(f"{BASE_URL}/cep/v2/{cep}")
    response.raise_for_status()
    data = response.json()
    return {
        "cep": data.get("cep"),
        "rua": data.get("street"),
        "latitude": data.get("location", {}).get("coordinates", {}).get("latitude"),
        "longitude": data.get("location", {}).get("coordinates", {}).get("longitude"),
        "bairro": data.get("neighborhood"),
        "cidade": data.get("city"),
        "estado": data.get("state"),
    }


async def buscar_cnpj(cnpj: str) -> dict:
    response = await _client.get(f"{BASE_URL}/cnpj/v1/{cnpj}")
    response.raise_for_status()
    data = response.json()
    return {
        "cnpj": data.get("cnpj"),
        "razao_social": data.get("razao_social"),
        "nome_fantasia": data.get("nome_fantasia"),
        "cnae_principal": str(data.get("cnae_fiscal", "")),
        "cnae_descricao": data.get("cnae_fiscal_descricao"),
        "capital_social": data.get("capital_social"),
        "natureza_juridica": data.get("natureza_juridica"),
        "porte": data.get("porte"),
        "situacao_cadastral": data.get("descricao_situacao_cadastral"),
        "data_abertura": data.get("data_inicio_atividade"),
        "logradouro": data.get("logradouro"),
        "numero": data.get("numero"),
        "complemento": data.get("complemento"),
        "bairro": data.get("bairro"),
        "cidade": data.get("municipio"),
        "estado": data.get("uf"),
        "cep": data.get("cep"),
        "telefone": data.get("ddd_telefone_1"),
    }
