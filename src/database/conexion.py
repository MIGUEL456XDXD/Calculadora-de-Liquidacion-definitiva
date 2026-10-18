
"""Conexión de SQLAlchemy con PostgreSQL."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "Configura la variable de entorno DATABASE_URL antes de ejecutar."
    )

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    """Clase base para los modelos ORM."""


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def crear_tablas() -> None:
    """Crea las tablas registradas en los modelos ORM."""
    Base.metadata.create_all(bind=engine)
