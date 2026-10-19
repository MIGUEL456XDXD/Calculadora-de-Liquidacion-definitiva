"""Conexión de SQLAlchemy con PostgreSQL."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

try:
    import secret_config  # type: ignore
    DATABASE_URL = getattr(secret_config, "DATABASE_URL", None)
except ImportError:
    DATABASE_URL = None

if not DATABASE_URL:
    DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "Configura secret_config.py o la variable de entorno DATABASE_URL "
        "antes de ejecutar."
    )

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    """Clase base para los modelos ORM."""


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)
