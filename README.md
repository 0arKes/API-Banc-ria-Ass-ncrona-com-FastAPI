# API Bancária Assíncrona com FastAPI

Esse é o meu resultado para o desafio do bootcamp **API Backend 2ª Edição - Luizalabs**. Que consiste em uma aplicação backend desenvolvida com FastAPI, utilizando arquitetura assíncrona em Python. [Link para o desafio](https://github.com/digitalinnovationone/trilha-python-dio/tree/main/13%20-%20APIs%20Assíncronas%20com%20FastAPI/desafio)

## 📌 Sumário

- [📖 Sobre o Projeto](#-sobre-o-projeto)
- [🚀 Funcionalidades](#-funcionalidades)
- [🛠 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [🏗 Arquitetura](#-arquitetura)
- [⚙️ Configuração do Ambiente](#️-configuração-do-ambiente)
- [📡 Endpoints](#-endpoints)


## 📖 Sobre o Projeto

O projeto simula operações bancárias básicas, permitindo:

- Cadastro de usuários
- Autenticação com JWT
- Criação de contas bancárias
- Depósitos e saques
- Consulta de extratos
- Controle de acesso por usuário

Escolhi o **PostgreSQL** como banco de dados principal (sqlite utilizado apenas no desenvolvimento e testes) pela sua maior confiabilidade, e desempenho.

> Algumas rotas `GET` foram mantidas públicas intencionalmente para fins didáticos e demonstração da API em ambiente de portfólio.

## 🚀 Funcionalidades

A API foi estruturada em módulos independentes. Cada segmento possuiu um arquivo `.py` na pasta routers, confira a estrutura em [🏗 Arquitetura](#-arquitetura) e as rotas em [📡 Endpoints](#-endpoints)

### 👤 Gerenciamento de Usuários

Gerencia Usuarios da api

[🚩Rota de Usuários](#-rota-usuários)

#### Funcionalidades

- Cadastro de usuários `POST` em `/user`
- Validação de e-mail via tipo `e-mail` do pydantic
- Senhas criptografadas com hash. Mais em [security.py](#-securitypy)
- Atualização de dados cadastrais `PUT` em `/user` -> apenas senha
- Exclusão de contas `DELETE` em `/user`
- Listagem de usuários `GET` em `/user`

---

### 🔐 Autenticação JWT

Controle de acesso utilizando autenticação baseada em JSON Web Token.

[🚩Rotas de Autenticação](#-autenticação--token)

#### Funcionalidades

- Login com JWT -> Seguro e rápido
- Proteção de rotas privadas aparecem com 🔒 no `/docs`
- Controle de autorização por usuário -> validação para rotas que exigem autenticação
- Tokens do tipo **Bearer**
- Validação de credenciais. Mais em [security.py](#-securitypy)

---

### 🏦 Gerenciamento de Contas Bancárias

Módulo responsável pelo gerenciamento das contas bancárias.

[🚩Rotas de Contas Bancárias](#-contas-bancárias)

#### Funcionalidades

- Criação de contas bancárias `POST` em `/bank`
- Associação automática ao usuário autenticado -> parte lógica da view
- Consulta de saldo e de extrato `GET` em `/bank{id}`

>Não há rotas de PUT, porque não há dados que o usuário pode modificar. E não há DELETE porque julguei que seria desnecessário. A maneira de deletar a conta bancária é excluindo o usuário, o que, por sua vez, exclui a conta bancária e seus dados relacionados, baseado na lógica _Cascade_.

---

### 💸 Transações Bancárias

Guarda as transações como um histórico.

#### Funcionalidades

- Depósitos `POST` em `/transaction`
- Saques `POST` em `/transaction`
- Atualização automática de saldo. Logica da view
- Validação de saldo insuficiente. Logica da view
- Histórico de transações. Registra numa tabela própria no DB
- Controle de acesso por proprietário da conta. 

---

### 📄 Paginação de Resultados

Listagem otimizada utilizando parâmetros de paginação.

#### Funcionalidades

- `offset`
- `limit`
- -> Controle de quantidade de registros retornados

O controle vem atravez do `utility_schemas.py`

```Python
from pydantic import BaseModel, Field


class FilterPage(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1)

```
---

### 🧪 Testes Automatizados

Como desafio extra. Resolvi utilizar o Pytest para escrever testes simples da API.

#### Funcionalidades

- Testes de rotas
- Testes de autenticação
- Testes de regras de negócio
- Fixtures reutilizáveis
- Banco de dados isolado para testes
- Testes assíncronos

---

## 🛠 Tecnologias Utilizadas

### ⚙️ Backend

- Python 3.14
- FastAPI
- Pydantic Settings
- SQLAlchemy Async
- Alembic
- PyJWT
- pwdlib
- Argon2
- tzdata

---

### 🗄 Banco de Dados

- PostgreSQL
- asyncpg `drive`

- SQLite (desenvolvimento e testes apenas)
- aiosqlite `drive`

---

### 🧪 Testes Automatizados

- Pytest
- Pytest Asyncio
- Pytest Cov
- FastAPI TestClient

---

### 🧹 Código

- Ruff
- Taskipy

---

### 🐳 DevOps & Infraestrutura

- Docker
- Docker Compose
- GitHub Actions
- Render

---

### 📦 Gerenciamento de Dependências

- Poetry

## 🏗 Arquitetura

### 📂 Estrutura Geral do Projeto

```text
.
├── .github/
│   └── workflows/
│       └── pipeline.yaml
│
├── BackendAPI/
│   ├── backendapi/
│   │   ├── models/ > Contém os modelos ORM do SQLAlchemy.
│   │   ├── routers/ > Responsável pelas rotas da API e comunicação HTTP.
│   │   ├── schemas/ > Responsável pela validação e serialização dos dados
│   │   ├── app.py > Arquivo de start da aplicação
│   │   ├── database.py > Responsável pela criação do engine assíncrono
│   │   ├── security.py > Centraliza toda lógica de autenticação e segurança da aplicação.
│   │   └── settings.py > Gerencia as variaveis de ambiente
│   │
│   ├── migrations/ > Diretório gerenciado pelo Alembic para versionamento do DB
│   │   └── versions/
│   │
│   ├── tests/ > Contém toda estrutura de testes automatizados da aplicação
│   │
│   ├── pyproject.toml > Contem as bibliotecas utilizadas no projeto
│   └── alembic.ini
│
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🧩 Organização dos Módulos

### 📡 `routers/`

Cada arquivo representa um domínio específico da aplicação:

- `user.py` → gerenciamento de usuários
- `token.py` → autenticação JWT
- `bank.py` → contas bancárias
- `transactions.py` → movimentações financeiras

---

### 🗄 `models/`

Aqui contem:

- Estrutura do DB
- As Chaves estrangeiras
- Demais configurações relacionadas ao ORM

---

### ✅ `schemas/`

Os schemas controlam:

- Entrada de dados
- Respostas da API
- Tipagem
- Segurança de informações expostas

---

### 🔐 `security.py`

Resposavel pela lógica de segurança

Inclui:

- Geração de JWT
- Verificação de token
- Hash de senhas
- Autenticação de usuários
- Controle de acesso

---

### ⚙️ `settings.py`

Gerencia as seguintes variáveis de ambiente:

- URL do banco
- Secret Key
- Algoritmo JWT
- Tempo de expiração do token

---

### 🧪 `tests/`

Inclui:

- Fixtures reutilizáveis
- Banco em memória
- Testes de autenticação
- Testes de regras de negócio
- Testes de rotas protegidas
- Testes assíncronos

---

## ⚙️ Configuração do Ambiente

Siga os passos abaixo para executar a aplicação localmente.

---

## 📥 Clonando o Repositório

```bash
git clone https://github.com/0arKes/API-Bancaria-Assincrona-com-FastAPI.git
```

```bash
cd API-Bancaria-Assincrona-com-FastAPI/BackendAPI
```

---

## 📦 Instalando as Dependências

O projeto utiliza o **Poetry** para gerenciamento de dependências.

### Instale o Poetry

```bash
pip install poetry
```

### Instale as dependências do projeto

```bash
poetry install
```

---

## 🔐 Configurando Variáveis de Ambiente

Crie um arquivo `.env` dentro da pasta `BackendAPI/`.

### Variáveis:

```env
DATABASE_URL=url_aqui
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🗄 Executando as Migrations

Execute as migrations do banco de dados:

```bash
poetry run alembic upgrade head
```

---

## ▶️ Executando a Aplicação

```bash
poetry run task run
```

-> Execução através da contração do task ['fastapi dev BackendAPI/app.py']

A aplicação estará disponível em:

```text
http://127.0.0.1:8000
```

---

## 📚 Documentação Automática

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

## 🧪 Executando os Testes

Para executar os testes automatizados:

```bash
poetry run task test
```

-> Execução através da contração do task ['pytest -s -x --cov=BackendAPI -vv']

---

