import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from alembic import op
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

from app.db.base_class import Base

load_dotenv()
config = context.config


fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:

    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL is not set")

    # force async driver is missing
    if not url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:

    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL is not set")

    # force async driver is missing
    if not url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://")


    connectable = create_async_engine(
        url, poolclass=pool.NullPool
    )

    async def run_async_migration():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations())

    def do_run_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

    import asyncio
    asyncio.run(run_async_migration())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
