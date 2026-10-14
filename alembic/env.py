from logging.config import fileConfig

from alembic import context
from sqlmodel import SQLModel

import app.modelos  # noqa: F401  (registra las tablas en SQLModel.metadata)
from app.config import config as config_app
from app.db import crear_engine

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

target_metadata = SQLModel.metadata

# La URL de alembic.ini está vacía: se usa la de la app, salvo que alguien
# (por ejemplo, los tests) la sobreescriba con set_main_option.
url = config.get_main_option("sqlalchemy.url") or config_app.database_url


def run_migrations_offline() -> None:
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = crear_engine(url)

    with connectable.connect() as connection:
        # render_as_batch: SQLite no soporta ALTER TABLE completo.
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
