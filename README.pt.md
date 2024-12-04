
[![Português](https://img.shields.io/badge/PT-blue)](README.pt.md)
[![English](https://img.shields.io/badge/EN-blue)](README.md)

# WorkoutAPI

Este é um projeto baseado em FastAPI para gerenciar atletas em uma competição de crossfit. Foi projetado pela instrutora da [dio](https://web.dio.me/home) **Nayanna Nara** como um projeto prático. Ele fornece endpoints para operações CRUD, filtragem e paginação, além de lidar graciosamente com problemas de integridade de dados. A API foi construída com boas práticas modernas, tornando-a rápida, escalável e fácil de usar.

## Funcionalidades

- Adicionar, atualizar, deletar e consultar dados de atletas.
- Filtrar atletas por `nome` e `cpf` utilizando parâmetros de consulta.
- Respostas personalizadas para listar atletas com informações relacionadas (`centro_treinamento` e `categoria`).
- Paginação com os parâmetros `limit` e `offset`.
- Tratamento adequado de entradas duplicadas com mensagens de erro descritivas.
- Documentação disponível via Swagger UI e ReDoc.

## Stack Tecnológica

- **FastAPI**: Para construção da API.
- **SQLAlchemy**: Para interação com o banco de dados.
- **Alembic**: Para gerenciar migrações do banco de dados.
- **Pydantic**: Para validação e serialização de dados.
- **PostgreSQL**: Como banco de dados.
- **Docker**: Para implantação containerizada.
- **fastapi-pagination**: Para lidar com paginação nos endpoints.

## Instruções de Configuração

Siga estas etapas para configurar e executar o projeto localmente.

## Pré-requisitos

- Python 3.9 ou superior
- Docker e Docker Compose instalados
- PostgreSQL instalado localmente ou via Docker

Para executar o projeto, utilizei [pyenv](https://github.com/pyenv/pyenv) com a versão 3.11.4 do Python para o ambiente virtual.

Caso opte por usar pyenv, após instalar, execute:

```bash
pyenv virtualenv 3.11.4 workoutapi
pyenv activate workoutapi
pip install -r requirements.txt
```
Para subir o banco de dados, caso não tenha o [docker-compose](https://docs.docker.com/compose/install/linux/) instalado, faça a instalação e logo em seguida, execute:

```bash
make run-docker
```
Para criar uma migration nova, execute:

```bash
make create-migrations d="nome_da_migration"
```

Para criar o banco de dados, execute:

```bash
make run-migrations
```

## API

Para subir a API, execute:
```bash
make run
```
e acesse: http://localhost:8000/docs

## Endpoints

### Endpoints de Atletas
- `GET /`: Lista todos os atletas com filtros opcionais e paginação.
  - **Parâmetros de Consulta**:
    - `limit`: Número de resultados a serem retornados.
    - `offset`: Número de resultados a serem ignorados.
    - `nome`: Filtrar pelo nome do atleta.
    - `cpf`: Filtrar pelo CPF do atleta.
  - **Resposta**:
    ```json
    {
        "items": [
            {
                "nome": "Joao",
                "centro_treinamento": {"nome": "Centro A"},
                "categoria": {"nome": "Categoria X"}
            }
        ],
        "limit": 5,
        "offset": 0,
        "total": 10
    }
    ```

- `POST /`: Adiciona um novo atleta.
  - **Corpo da Requisição**:
    ```json
    {
        "nome": "Joao",
        "cpf": "12345678901",
        "idade": 25,
        "peso": 75.5,
        "altura": 170.0,
        "sexo": "M",
        "categoria": {"nome": "Categoria X"},
        "centro_treinamento": {"nome": "Centro A"}
    }
    ```

- `PATCH /{id}`: Atualiza informações de um atleta com base no ID.
- `DELETE /{id}`: Remove um atleta com base no ID.

### Tratamento de Erros
- `IntegrityError`: Mensagem de erro personalizada para CPF duplicado.
  - **Resposta**:
    ```json
    {
        "detail": "Já existe um atleta cadastrado com o cpf: 12345678901"
    }
    ```

### Paginação
- Os parâmetros `limit` e `offset` estão disponíveis nos endpoints de listagem para suporte à paginação.

## Testes

- Utilize o Swagger UI em: [http://localhost:8000/docs](http://localhost:8000/docs).
- Utilize o módulo `requests` do Python:
    ```python
    import requests

    url = "http://localhost:8000/?limit=5&offset=10"
    response = requests.get(url)
    print(response.json())
    ```

## Referências

- [Documentação do FastAPI](https://fastapi.tiangolo.com/)
- [Documentação do SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentação do Pydantic](https://docs.pydantic.dev/)
- [Documentação do Docker](https://docs.docker.com/)
- [Documentação do Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Documentação do Fastapi-pagination](https://uriyyo-fastapi-pagination.netlify.app/)
