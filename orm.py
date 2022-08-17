"""Main orm connection settings and db initialization."""

from config import settings

DEFAULT_CONNECTION = "postgres://{0}:{1}@{2}:5432/{3}".format(
    settings.postgres_user,
    settings.postgres_password,
    settings.postgres_server,
    settings.postgres_db,
)

TORTOISE_ORM = {
    "connections": {"default": DEFAULT_CONNECTION},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
