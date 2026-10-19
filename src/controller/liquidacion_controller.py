"""Funciones para administrar liquidaciones en la base de datos."""

from datetime import date
from decimal import Decimal
from typing import Optional

from src.database.conexion import Base, SessionLocal, engine
from src.model.modelo_liquidacion import ModeloLiquidacion


def crear_tablas() -> None:
    """Crea las tablas necesarias en la base de datos."""
    Base.metadata.create_all(bind=engine)


def borrar_tablas() -> None:
    """Elimina las tablas definidas en los modelos."""
    Base.metadata.drop_all(bind=engine)


def insertar_liquidacion(
    fecha_ingreso: date,
    fecha_retiro: date,
    salario: Decimal,
    dias_trabajados: int,
    salario_integral: bool,
) -> int:
    """Guarda una liquidación y devuelve su identificador."""
    if fecha_retiro < fecha_ingreso:
        raise ValueError("El retiro no puede ser anterior al ingreso.")

    if salario <= 0:
        raise ValueError("El salario debe ser mayor que cero.")

    if dias_trabajados <= 0:
        raise ValueError("Los días trabajados deben ser mayores que cero.")

    with SessionLocal() as session:
        liquidacion = ModeloLiquidacion(
            fecha_ingreso=fecha_ingreso,
            fecha_retiro=fecha_retiro,
            salario=salario,
            dias_trabajados=dias_trabajados,
            salario_integral=salario_integral,
        )
        session.add(liquidacion)
        session.commit()
        session.refresh(liquidacion)
        return liquidacion.id


def buscar_liquidacion(identificador: int) -> Optional[ModeloLiquidacion]:
    """Busca una liquidación por su identificador."""
    if not isinstance(identificador, int) or identificador <= 0:
        raise ValueError("El identificador debe ser un entero mayor que cero.")

    with SessionLocal() as session:
        return session.get(ModeloLiquidacion, identificador)


def listar_liquidaciones() -> list[ModeloLiquidacion]:
    """Devuelve todas las liquidaciones guardadas."""
    with SessionLocal() as session:
        return list(
            session.query(ModeloLiquidacion)
            .order_by(ModeloLiquidacion.id)
            .all()
        )


def eliminar_liquidacion(identificador: int) -> bool:
    """Elimina una liquidación. Devuelve False si no existe."""
    if not isinstance(identificador, int) or identificador <= 0:
        raise ValueError("El identificador debe ser un entero mayor que cero.")

    with SessionLocal() as session:
        liquidacion = session.get(ModeloLiquidacion, identificador)

        if liquidacion is None:
            return False

        session.delete(liquidacion)
        session.commit()
        return True
