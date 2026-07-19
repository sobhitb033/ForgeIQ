from logging.config import fileConfig
from urllib.parse import quote_plus

from sqlalchemy import create_engine, pool
from alembic import context

from app.core.config import settings
from app.database.base import Base

import app.models

# Import all models here so Alembic can detect them
# Example:
# from app.models.user import User

config = context.config

# Build database URL from settings
DATABASE_URL = (
    f"mysql+pymysql://"
    f"{quote_plus(settings.DB_USER)}:"
    f"{quote_plus(settings.DB_PASSWORD)}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

config.set_main_option("sqlalchemy.url", DATABASE_URL.replace("%", "%%"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()