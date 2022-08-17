# FASTAPI BENCHMARK

Comparison of the FastAPI application response rate:

- Tortoise ORM:
    - Base pydantic models
    - Models with orjson
    - Orjson response
- Tortoise values:
    - Base pydantic models
    - Models with orjson
    - Orjson response
- Asyncpg:
    - Base pydantic models
    - Models with orjson
    - Orjson response


### Install dependencies 

```
poetry install
```

### Copy data from MS SQL to PostgreSQL

- Install Microsoft [ODBC](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15) driver for SQL Server,
- Set right driver version in MSSQL DNS,

```
poetry run mssql2postgres.py
```

### Run server

```
poetry run uvicorn server:app
```
### Run client

```
poetry run client.py
```
