from pydantic import BaseSettings


class Settings(BaseSettings):
    mssql_server: str
    mssql_db: str
    mssql_username: str
    mssql_password: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_server: str

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
