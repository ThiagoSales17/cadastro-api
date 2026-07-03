CREATE TYPE tipo_cliente AS ENUM ('PF', 'PJ');

CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    tipo tipo_cliente NOT NULL,
    cpf_cnpj VARCHAR(14) UNIQUE NOT NULL,
    nome_razao_social VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    telefone VARCHAR(20),
    cep VARCHAR(8),
    rua VARCHAR(255),
    numero VARCHAR(10),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado CHAR(2),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabela exclusiva para PJ (1:1 com clientes)
CREATE TABLE campos_pj (
    id SERIAL PRIMARY KEY,
    cliente_id INT UNIQUE NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    nome_fantasia VARCHAR(255),
    cnae_principal VARCHAR(7),
    cnae_descricao VARCHAR(255),
    capital_social DECIMAL(15, 2),
    natureza_juridica VARCHAR(255),
    porte VARCHAR(50),
    situacao_cadastral VARCHAR(50),
    data_abertura DATE
);

CREATE TABLE cache_brasil_api (
    chave VARCHAR(100) PRIMARY KEY,  -- "cep:01001000" ou "cnpj:00000000000191"
    dados JSONB NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);