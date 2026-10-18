
"""Pruebas del controlador de liquidaciones."""

from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import inspect

from src.database.conexion import engine
from src.controller.liquidacion_controller import (
    crear_tablas,
    borrar_tablas,
    insertar_liquidacion,
    buscar_liquidacion,
    eliminar_liquidacion,
)


@pytest.fixture
def base_datos():
    """Prepara las tablas para ejecutar las pruebas."""
    crear_tablas()
    yield


def test_insertar_liquidacion_correcta(base_datos):
    """Comprueba que se pueda guardar una liquidación."""
    identificador = insertar_liquidacion(
        date(2024, 1, 1),
        date(2024, 12, 31),
        Decimal("2000000.00"),
        360,
        False,
    )

    try:
        assert identificador > 0
    finally:
        eliminar_liquidacion(identificador)


def test_buscar_liquidacion_existente(base_datos):
    """Comprueba que se encuentre una liquidación guardada."""
    identificador = insertar_liquidacion(
        date(2024, 1, 1),
        date(2024, 12, 31),
        Decimal("2500000.00"),
        360,
        False,
    )

    try:
        resultado = buscar_liquidacion(identificador)

        assert resultado is not None
        assert resultado.id == identificador
        assert resultado.salario == Decimal("2500000.00")
    finally:
        eliminar_liquidacion(identificador)


def test_buscar_liquidacion_inexistente(base_datos):
    """Comprueba qué ocurre cuando el registro no existe."""
    resultado = buscar_liquidacion(-999)

    assert resultado is None


def test_insertar_salario_invalido(base_datos):
    """Comprueba que no se acepte un salario de cero."""
    with pytest.raises(ValueError):
        insertar_liquidacion(
            date(2024, 1, 1),
            date(2024, 12, 31),
            Decimal("0"),
            360,
            False,
        )


def test_insertar_fecha_retiro_anterior(base_datos):
    """Comprueba que el retiro no sea anterior al ingreso."""
    with pytest.raises(ValueError):
        insertar_liquidacion(
            date(2024, 12, 31),
            date(2024, 1, 1),
            Decimal("2000000.00"),
            360,
            False,
        )


def test_insertar_dias_trabajados_invalidos(base_datos):
    """Comprueba que no se acepten días trabajados inválidos."""
    with pytest.raises(ValueError):
        insertar_liquidacion(
            date(2024, 1, 1),
            date(2024, 12, 31),
            Decimal("2000000.00"),
            0,
            False,
        )


def test_eliminar_liquidacion_existente(base_datos):
    """Comprueba que se pueda eliminar una liquidación."""
    identificador = insertar_liquidacion(
        date(2024, 1, 1),
        date(2024, 12, 31),
        Decimal("2000000.00"),
        360,
        False,
    )

    assert eliminar_liquidacion(identificador) is True
    assert buscar_liquidacion(identificador) is None


def test_eliminar_liquidacion_inexistente(base_datos):
    """Comprueba que no se elimine un registro que no existe."""
    assert eliminar_liquidacion(-999) is False


def test_crear_tablas(base_datos):
    """Comprueba que exista la tabla de liquidaciones."""
    assert inspect(engine).has_table("liquidaciones")


def test_borrar_tablas(base_datos):
    """Comprueba que se puedan borrar las tablas."""
    borrar_tablas()

    assert not inspect(engine).has_table("liquidaciones")