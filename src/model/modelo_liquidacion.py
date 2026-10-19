"""Modelo ORM para almacenar liquidaciones definitivas."""

from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from src.database.conexion import Base


class ModeloLiquidacion(Base):
    """Representa una liquidación definitiva en la base de datos."""

    __tablename__ = "liquidaciones"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    fecha_ingreso: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_retiro: Mapped[date] = mapped_column(Date, nullable=False)
    salario: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    dias_trabajados: Mapped[int] = mapped_column(Integer, nullable=False)
    salario_integral: Mapped[bool] = mapped_column(Boolean, nullable=False)
