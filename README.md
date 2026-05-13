# API Bancária Assíncrona com FastAPI

Esse é o meu resultado para o desafio do bootcamp **API Backend 2ª Edição - Luizalabs**. Que consiste em uma aplicação backend desenvolvida com FastAPI, utilizando arquitetura assíncrona em Python. [Link para o desafio](https://github.com/digitalinnovationone/trilha-python-dio/tree/main/13%20-%20APIs%20Assíncronas%20com%20FastAPI/desafio)

## 📌 Sumário

- [📖 Sobre o Projeto](#-sobre-o-projeto)
- [🚀 Funcionalidades](#-funcionalidades)
- [🛠 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [🏗 Arquitetura](#-arquitetura)
- [🎲 Banco de Dados](#-banco-de-dados)
- [📡 Endpoints](#-endpoints)
- [⚙️ Configuração do Ambiente](#️-configuração-do-ambiente)

## 📖 Sobre o Projeto

O projeto simula operações bancárias básicas, permitindo:

- Cadastro de usuários
- Cadastro de contas bancárias
- Controle de acesso por usuário
- Autenticação com JWT
- Depósitos e saques
- Consulta de extratos
- Histórico de operações


Escolhi o **PostgreSQL** como banco de dados principal (sqlite utilizado apenas no desenvolvimento e testes) pela sua maior confiabilidade, e desempenho.

> Algumas rotas `GET` foram mantidas públicas intencionalmente para fins didáticos e demonstração da API em ambiente de portfólio.

## 🚀 Funcionalidades

A API foi estruturada em módulos independentes. Cada segmento possui um arquivo `.py` na pasta routers, confira a estrutura em [🏗 Arquitetura](#-arquitetura) e as rotas em [📡 Endpoints](#-endpoints)

### 👤 Gerenciamento de Usuários

Endpoint responsável por gerenciar Usuários da api

[🚩Rota de Usuários](#-users--user)

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

[🚩Rotas de Autenticação](#-token--token)

#### Funcionalidades

- Login com JWT -> Seguro e rápido
- Proteção de rotas privadas aparecem com 🔒 no `/docs`
- Controle de autorização por usuário -> validação para rotas que exigem autenticação
- Tokens do tipo **Bearer**
- Validação de credenciais. Confira em [security.py](#-securitypy)

---

### 🏦 Gerenciamento de Contas Bancárias

Módulo responsável pelo gerenciamento das contas bancárias.

[🚩Rotas de Contas Bancárias](#-bank--bank)

#### Funcionalidades

- Criação de contas bancárias `POST` em `/bank`
- Associação automática ao usuário autenticado -> lógica implementada na rota
- Consulta de saldo e de extrato `GET` em `/bank{id}`

>Não há rotas de PUT, porque não há dados que o usuário pode modificar. E não há DELETE porque julguei que seria desnecessário. A maneira de deletar a conta bancária é excluindo o usuário, o que, por sua vez, exclui a conta bancária e seus dados relacionados, baseado na lógica _Cascade_ da tabela.

---

### 💸 Transações Bancárias

Guarda as transações como um histórico.

[🚩Rotas de Transações Bancárias](#-transactions--transaction)

#### Funcionalidades

- Saques e Depósitos `POST` em `/transaction`
- Atualização automática de saldo. -> Antes de ser registrada, a transação tenta atualizar o `balance` pertencente ao usuário que faz a requisição.
- Validação de saldo insuficiente. -> Invalida caso o usuario tente tirar mais do que possui em `balance`
- Histórico de transações. Registra numa tabela própria no Banco de Dados

---

### 📄 Paginação de Resultados

Para a listagem otimizada utilizando parâmetros de paginação. Optei por usar um schema

#### Funcionalidades

- `offset`
- `limit`
- -> Controle de quantidade de registros retornados

O controle vem através do `utility_schemas.py`

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

## 🛠 Tecnologias Utilizadas

### ⚙️ Backend

- **Python 3.14**
- **FastAPI** — Escolhi pela simplicidade, performance e documentação automática da API.
- **SQLAlchemy Async** — Para facilitar o desenvolvimento e a troca de banco de dados
- **Alembic** — Para versionar e controlar migrações do banco de dados.
- **PyJWT** — Utilizado na autenticação baseada em tokens JWT.
- **pwdlib** — Para simplificar o gerenciamento e verificação de senhas.
- **Argon2** — Escolhido por ser um algoritmo moderno e seguro para hash de senhas.

---

### 🗄 Sobre o Banco de Dados

- **PostgreSQL**
- **asyncpg** `driver` -> escolhido porque permite conexões assíncronas de alta performance com PostgreSQL

- **SQLite** (desenvolvimento e testes apenas)
- **aiosqlite** `driver`

---

### 🧪 Testes Automatizados

- **Pytest** — Utilizado para garantir a qualidade e confiabilidade da aplicação através de testes automatizados.

---

### 🧹 Código

- Ruff

Configuração:
```py
[tool.ruff]
line-length = 79 #PEP 8
extend-exclude = ['migrations'] # não mexe nas migrations

[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT', 'FAST'] # verificações

[tool.ruff.format]
preview = true
quote-style = 'single' # tipo de str
```

- Taskipy

Configuração:
```py
[tool.taskipy.tasks] # comandos que podem ser encurtados com task
lint = 'ruff check'
pre_format = 'ruff check --fix'
format = 'ruff format'
run = 'fastapi dev BackendAPI/app.py'
pre_test = 'task lint'
test = 'pytest -s -x --cov=BackendAPI -vv'
post_test = 'coverage html'
```

---

### 🐳 DevOps & Infraestrutura

- **Docker**
- **Docker Compose**
- **GitHub Actions**
- **Render** [🔗 Resultado final](https://api-bancaria-assincrona-com-fastapi.onrender.com)

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
│   │   └── settings.py > Gerencia as variáveis de ambiente
│   │
│   ├── migrations/ > Diretório gerenciado pelo Alembic para versionamento do DB
│   │   └── versions/
│   │
│   ├── tests/ > Contém toda estrutura de testes automatizados da aplicação
│   │
│   ├── pyproject.toml > Contém as bibliotecas utilizadas no projeto
│   └── alembic.ini
│
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🧩 Organização dos Módulos

### 📡 `routers/`

Cada arquivo representa um domínio específico da aplicação:

- `user.py` → gerenciamento de usuários
- `token.py` → autenticação JWT
- `bank.py` → contas bancárias
- `transactions.py` → movimentações financeiras

---

### 🗄 `models/`

Aqui contém:

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

Responsável pela lógica de segurança

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

# 🎲 Banco de Dados

Escolhi o SQLAlchemy como ORM para gerenciar a entrada e saída de dados da aplicação.

# 📳 Modelagem

```text
User
 └── BankAccount
       └── Transaction
```

# 👥 Tabela: `users`

Responsável pelo armazenamento dos usuários da plataforma.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | `int` | Identificador do usuário [único, PK] |
| `email` | `str` | Email utilizado para autenticação [único] |
| `password` | `str` | Senha criptografada do usuário |
| `cpf` | `str` | Documento de identificação [único] |
| `created_at` | `datetime` | Data de criação do registro |


### 🔴 OBS: `created_at`

```python
server_default = func.now()
```

A data é gerada automaticamente pelo banco de dados no momento da criação do registro.

---

# 🏦 Tabela: `bank_account`

Representa as contas bancárias vinculadas aos usuários.

| Campo | Tipo | Descrição |
|---|---|---|
| `account_id` | `int` | Identificador da conta [único, PK] |
| `owner_id` | `int` | Referência ao proprietário da conta [FK de users.id]|
| `balance` | `float` | Saldo atual da conta (mantido float apenas para uso didático)|

---

# 💸 Tabela: `transaction`

Armazena todas as movimentações realizadas nas contas bancárias.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | `int` | Identificador da transação [único, PK] |
| `account_id` | `int` | Conta relacionada [FK de bank_account.account_id] |
| `type_transaction` | `TransactionType` | Tipo da movimentação |
| `amount` | `float` | Valor da operação |
| `created_at` | `datetime` | Data da transação |

### `type_transaction`

```python
class TransactionType(str, Enum):
    deposit = 'deposit'
    withdrawal = 'withdrawal'
```

Utilizei `Enum` para impedir valores inválidos da transação no banco.

Tipos disponíveis:

- `deposit`
- `withdrawal`

## 🔴 Cascade Delete

```python
cascade='all, delete-orphan'
```

Aplicado para manter integridade entre entidades relacionadas.

### Comportamento

- Remover um usuário remove suas contas
- Remover uma conta remove suas transações


## 🔴 Loading Strategy

```python
lazy='selectin'
```

Estratégia utilizada para otimizar carregamento de relacionamentos e reduzir problemas de N+1 queries.

## No Geral a modelagem foi construída utilizando:

- SQLAlchemy ORM
- `mapped_as_dataclass`
- Tipagem com `Mapped`
- Relacionamentos bidirecionais com `relationship`

# 📡 Endpoints

>para uma melhor visualização visite a documentação no Swagger

### 👤 Users — `/user`

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/user/` | Cria um novo usuário |
| `GET` | `/user/` | Lista os usuários cadastrados |
| `PUT` | `/user/{user_id}` | Atualiza a senha do usuário |
| `DELETE` | `/user/{user_id}` | Remove um usuário |


## Exemplo:

### 🔹 POST `/user/`

Cria um novo usuário na plataforma os campos de email e CPF são únicos.  
A senha enviada é protegida utilizando hash antes de ser salva no banco.

### Exemplo de envio

```json
{
  "email": "user@email.com",
  "password": "123456",
  "cpf": "12345678900"
}
```

### Exemplo de retorno

```json
{
  "email": "user@email.com",
  "id": 1
}
```

## 🔹 GET `/user/`

Retorna uma lista paginada de usuários cadastrados.

### Query Params

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `offset` | int | Define o ponto inicial da busca |
| `limit` | int | Quantidade máxima de registros |

### Exemplo

```http
GET /user/?offset=0&limit=10
```

### Exemplo de retorno

```json
{
  "users": [
    {
      "email": "user@email.com",
      "id": 1
    }
  ]
}
```

## 🔹 PUT `/user/{user_id}`

Atualiza a senha do usuário autenticado.  
A operação só pode ser realizada pelo próprio dono da conta.

### Exemplo de envio

```json
{
  "password": "novasenha123"
}
```

### Exemplo de retorno

```json
{
  "email": "user@email.com",
  "id": 1
}
```

# 🔐 Token — `/token`

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/token/` | Realiza autenticação e gera um JWT |

---

## 🔹 POST `/token/`

Responsável pelo login da aplicação.  
Valida email e senha e retorna um token JWT para acesso às rotas protegidas.


### Exemplo de envio

```json
{
  "username": "user@email.com",
  "password": "123456"
}
```

### Exemplo de retorno

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

# 🏦 Bank — `/bank`

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/bank/` | Cria uma conta bancária |
| `GET` | `/bank/{account_id}/` | Retorna o extrato da conta |

---

## 🔹 POST `/bank/`

Cria uma nova conta bancária vinculada ao usuário autenticado.


### Exemplo de envio

```json
{
  "balance": 1000
}
```

### Exemplo de retorno

```json
{
  "account_id": 1
}
```

---

## 🔹 GET `/bank/{account_id}/`

Retorna o saldo atual e o histórico de transações da conta.


### Exemplo de retorno

```json
{
  "balance": 850,
  "transactions": [
    {
      "account_id": 1,
      "type_transaction": "deposit",
      "amount": 1000,
      "created_at": "2026-04-13T15:30:00"
    }
  ]
}
```

---

# 💸 Transactions — `/transaction`

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/transaction/` | Realiza depósitos e saques |
| `GET` | `/transaction/` | Lista transações registradas |

## 🔹 POST `/transaction/`

Cria uma movimentação financeira em uma conta bancária.  
A rota suporta depósitos e saques, atualizando automaticamente o saldo da conta.


### Exemplo de envio

```json
{
  "account_id": 1,
  "type_transaction": "deposit",
  "amount": 500
}
```

### Exemplo de retorno

```json
{
  "account_id": 1,
  "type_transaction": "deposit",
  "amount": 500,
  "created_at": "2026-04-13T15:30:00"
}
```

## 🔹 GET `/transaction/`

Retorna uma lista paginada de transações registradas no sistema. **_Aqui é publico meramente por escolha didática_**

### Query Params

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `offset` | int | Define o ponto inicial |
| `limit` | int | Quantidade máxima de registros |

### Exemplo

```http
GET /transaction/?offset=0&limit=10
```

### Exemplo de retorno

```json
{
  "transactions": [
    {
      "account_id": 1,
      "type_transaction": "withdrawal",
      "amount": 100,
      "created_at": "2026-04-13T15:30:00"
    }
  ]
}
```

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

## 📚 Documentação Automática

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

## 🧪 Executando os Testes

Para executar os testes automatizados:

```bash
poetry run task test
```

-> Execução através da contração do task ['pytest -s -x --cov=BackendAPI -vv']

# Agradecimentos

Alguns objetivos do desafio foram adaptados para tornar o projeto mais interessante sob a minha perspectiva.

Agradeço ao professor [@guicarvalho](https://github.com/guicarvalho) pelas aulas e ao pessoal do Luizalabs pela oportunidade.

Mais projetos no meu perfil: [@0arKes](https://github.com/0arKes)
