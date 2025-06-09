# 🌾 Brain Agriculture

API REST para gestão de Agricultores, Fazendas, Culturas e Safras. Projeto desenvolvido em Flask com SQLAlchemy e Postgre seguindo princípios de Clean Architecture.

---

## 🐳 Como executar com Docker

### 1. Clone o repositorio

### 2. Suba os containers

```bash
docker-compose up --build
```

> A aplicação Flask será iniciada em `http://localhost:80`  
> O banco PostgreSQL estará acessível na porta `5432`

---
## 📚 Documentação
Casos de uso disponibilizados na pasta casos_de_uso contendo toda a API mapeada e configurada no postman
---

## 📁 Estrutura de Pastas (Clean Architecture)

```
src
├── app
│   ├── models
│   ├── resources
│   └── tests 
├── nginx
```

---

## ✅ Endpoints Disponíveis

### 🌾 Produtores

| Método | Rota              | Descrição                          |
| ------ | ----------------- | ---------------------------------- |
| POST   | /produtores       | Cadastra novo agricultor           |
| GET    | /produtores       | Lista todos os agricultores        |
| PUT    | /produtores       | Atualiza os dados de um agricultor |
| DELETE | /produtores       | Remove um agricultor               |

---

### 🏡 Fazendas

| Método | Rota          | Descrição                        |
| ------ | ------------- | -------------------------------- |
| POST   | /propriedades | Cadastra nova fazenda            |
| GET    | /propriedades | Lista todas as fazendas          |
| PUT    | /propriedades | Atualiza os dados de uma fazenda |
| DELETE | /propriedades | Remove uma fazenda               |

---

### 🌱 Produtos

| Método | Rota          | Descrição                        |
| ------ | ------------- | -------------------------------- |
| POST   | /produtos     | Cadastra nova cultura            |
| GET    | /produtos     | Lista todas as culturas          |
| PUT    | /produtos     | Atualiza os dados de uma cultura |
| DELETE | /produtos     | Remove uma cultura               |

---

### 🌾 Safras

| Método | Rota        | Descrição                      |
| ------ | ----------- | ------------------------------ |
| POST   | /safras     | Cadastra nova safra            |
| GET    | /safras     | Lista todas as safras          |
| PUT    | /safras     | Atualiza os dados de uma safra |
| DELETE | /safras     | Remove uma safra               |

---

## 🧱 Diagrama do Banco de Dados

```mermaid
erDiagram
    produtores {
        int produtor_id PK
        string cpf_cnpj
        string nome_Produtor
        string tipo_Produtor
        timestamp criado_em
        timestamp atualizado_em
    }

    propriedades {
        int propriedade_id PK
        int produtor_id FK
        string nome_Propriedade
        string cidade_Propriedade
        string estado_Propriedade
        float area_total_Propriedade
        float area_vegetacao_Propriedade
        float area_agricultavel_Propriedade
        timestamp criado_em
        timestamp atualizado_em
    }

    produtos {
        int id PK
        string nome_produto
        string descricao
        string categoria
        timestamp created_at
        timestamp updated_at
    }

    safras {
        int safra_id PK
        int propriedade_id FK
        int produtor_id FK
        int safra_produto_id FK
        int safra_ano
        int safra_area
        int safra_producao
        int safra_rendimento
        timestamp created_at
        timestamp updated_at
    }

    produtores ||--o{ propriedades : possui
    propriedades ||--o{ safras : possui
    produtos ||--o{ safras : possui

```
