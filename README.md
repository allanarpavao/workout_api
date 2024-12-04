
[![Português](https://img.shields.io/badge/PT-blue)](README.pt.md)
[![English](https://img.shields.io/badge/EN-blue)](README.md)

# WorkoutAPI

This is a FastAPI-based project for managing athletes in a crossfit competition. It was designed by [dio.](https://web.dio.me/home) instructor **Nayanna Nara** as a hands-on project. It provides endpoints for CRUD operations, filtering, and pagination, and handles data integrity issues gracefully. The API is built with modern best practices, making it fast, scalable, and easy to use.

## Features

- Add, update, delete, and query athlete data.
- Filter athletes by `nome` and `cpf` using query parameters.
- Custom responses for listing athletes with related information (`centro_treinamento` and `categoria`).
- Pagination with `limit` and `offset` query parameters.
- Graceful handling of duplicate entries with descriptive error messages.
- Documentation available via Swagger UI and ReDoc.

## Technology Stack

- **FastAPI**: For building the API.
- **SQLAlchemy**: For database interaction.
- **Alembic**: For managing database migrations.
- **Pydantic**: For data validation and serialization.
- **PostgreSQL**: As the database.
- **Docker**: For containerized deployment.
- **fastapi-pagination**: For handling pagination in endpoints.

## Setup Instructions

Follow these steps to set up and run the project locally.

## Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose installed
- PostgreSQL installed locally or via Docker

To run the project, I used [pyenv](https://github.com/pyenv/pyenv) with Python version 3.11.4 for the virtual environment.

If you choose to use pyenv, after installing it, execute:

```bash
pyenv virtualenv 3.11.4 workoutapi
pyenv activate workoutapi
pip install -r requirements.txt
```
To start the database, if you don't have docker-compose installed, install it and then execute:

```bash
make run-docker
```
To create a new migration, execute:

```bash
make create-migrations d="nome_da_migration"
```

To create the database, execute:

```bash
make run-migrations
```

## API

To start the API, execute:
```bash
make run
```
e access: http://localhost:8000/docs


## Endpoints

### Athlete Endpoints
- `GET /`: List all athletes with optional filters and pagination.
  - **Query Parameters**:
    - `limit`: Number of results to return.
    - `offset`: Number of results to skip.
    - `nome`: Filter by athlete name.
    - `cpf`: Filter by athlete CPF.
  - **Response**:
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

- `POST /`: Add a new athlete.
  - **Body**:
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

- `PATCH /{id}`: Update an athlete by ID.
- `DELETE /{id}`: Delete an athlete by ID.

### Error Handling
- `IntegrityError`: Custom error message for duplicate CPF.
  - **Response**:
    ```json
    {
        "detail": "Já existe um atleta cadastrado com o cpf: 12345678901"
    }
    ```

### Pagination
- `limit` and `offset` parameters are available on list endpoints for paginated responses.


## Testing

- Use Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Use Python's `requests` module:
    ```python
    import requests

    url = "http://localhost:8000/?limit=5&offset=10"
    response = requests.get(url)
    print(response.json())
    ```

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Documentation](https://docs.docker.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)
- [Fastapi-pagination Documentation](https://uriyyo-fastapi-pagination.netlify.app/)