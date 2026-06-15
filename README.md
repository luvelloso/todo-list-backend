# ToDo Backend

Backend da API de tarefas desenvolvido com FastAPI e SQLAlchemy.

## Visão geral

O backend oferece autenticação, cadastro de usuário, criação e listagem de tarefas, atualização de status e exclusão por ID.

## Estrutura principal

- `main.py` - define as rotas da API
- `models.py` - define os modelos de banco de dados e enums
- `schemas.py` - define os modelos Pydantic de requisição/resposta
- `auth.py` - funções de autenticação, hash de senha e geração de JWT
- `database.py` - configuração do SQLAlchemy
- `todo.db` - arquivo SQLite gerado pelo backend

## Requisitos

- Python 3.11+ (recomendado)
- virtualenv / venv
- Dependências:
  - `fastapi`
  - `uvicorn`
  - `sqlalchemy`
  - `pydantic[email]`
  - `bcrypt`
  - `PyJWT`

## Instalação

1. Crie e ative o ambiente virtual:

```bash
cd backend/todo-backend
python3 -m venv venv
source venv/bin/activate
```

2. Instale as dependências:

```bash
pip install fastapi uvicorn sqlalchemy "pydantic[email]" bcrypt PyJWT
```

## Executando

```bash
uvicorn main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`.

## Endpoints

### Autenticação e usuário

- `POST /register`
  - Cria um novo usuário com `email`, `full_name` e `password`.
  - Valida email válido, senha com maiúscula, número e caractere especial.

- `POST /login`
  - Autentica com `username` (e-mail) e `password`.
  - Retorna `access_token` e `token_type`.

- `GET /users/me`
  - Retorna os dados do usuário logado.
  - Requer header `Authorization: Bearer <token>`.

### Tarefas

- `POST /todos`
  - Cria uma tarefa com:
    - `title`
    - `category` (`design`, `personal`, `house`, `work`, `health`)
    - `status` (`pending` ou `completed`)
    - `scheduled_date` (formato `YYYY-MM-DD`)

- `GET /todos`
  - Lista todas as tarefas do usuário.
  - Query params opcionais:
    - `status` para filtrar por `pending` ou `completed`
    - `scheduled_date` para filtrar por data exata (`YYYY-MM-DD`)

- `GET /todos/{todo_id}`
  - Retorna tarefa específica por ID.

- `PUT /todos/{todo_id}/status`
  - Atualiza apenas o status da tarefa.
  - Body:

```json
{
  "status": "completed"
}
```

- `DELETE /todos/{todo_id}`
  - Exclui a tarefa pelo ID.

## Modelos de dados

### UserCreate

```json
{
  "email": "usuario@exemplo.com",
  "full_name": "Nome Completo",
  "password": "SenhaForte@1"
}
```

### TodoCreate

```json
{
  "title": "Tarefa exemplo",
  "category": "work",
  "status": "pending",
  "scheduled_date": "2026-06-15"
}
```

### TodoStatusUpdate

```json
{
  "status": "completed"
}
```

## Sugestões de commit

Use mensagens pequenas, claras e consistentes.

### Padrão recomendado

- `feat: adicionar rota de cadastro e login`
- `fix: corrigir validação de senha no cadastro`
- `refactor: remover descrição da tarefa e adicionar categoria`
- `docs: criar README do backend`
- `test: adicionar testes para endpoint de listagem`
- `chore: atualizar dependências do projeto`

### Exemplo de fluxo

1. `feat: implementar criação de tarefa com categoria e data`
2. `fix: ajustar filtro de listagem por data e status`
3. `refactor: deixar endpoint de atualização só para status`
4. `docs: documentar endpoints no README`

## Observações

- A API usa SQLite local (`todo.db`), então o banco é gerado automaticamente na primeira execução.
- Se mudar o esquema do modelo, pode ser necessário excluir `todo.db` para recriar a tabela.
