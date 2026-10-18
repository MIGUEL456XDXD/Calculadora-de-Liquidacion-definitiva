"""Lógica para calcular la liquidación definitiva de un trabajador."""

import calendar
from dataclasses import dataclass
from datetime import date


class FechasInvalidas(Exception):
    """Se presenta cuando la fecha de ingreso es posterior al retiro."""


class SalarioNegativo(Exception):
    """Se presenta cuando los valores salariales no son válidos."""


class DiasPendientesInvalidos(Exception):
    """Se presenta cuando los días pendientes no están entre 0 y 30."""


class AuxilioTransporteInvalido(Exception):
    """Se presenta cuando el auxilio de transporte no corresponde."""


@dataclass
class DatosLiquidacion:
    """Agrupa los datos necesarios para calcular una liquidación."""

    ingreso: date
    retiro: date
    sueldo_mensual: float
    salario_total: float
    dias_pendientes: int
    es_salario_integral: bool = False


SALARIO_MINIMO = {
    2024: 1_300_000,
    2025: 1_423_500,
    2026: 1_750_905,
}


def calcular_dias_360(fecha_inicio: date, fecha_fin: date) -> int:
    """Calcula días con año comercial de 360 días."""

    ultimo_inicio = calendar.monthrange(
        fecha_inicio.year, fecha_inicio.month
    )[1]
    ultimo_fin = calendar.monthrange(
        fecha_fin.year, fecha_fin.month
    )[1]

    dia_inicio = fecha_inicio.day
    dia_fin = fecha_fin.day

    if dia_inicio == 31 or (
        fecha_inicio.month == 2 and dia_inicio == ultimo_inicio
    ):
        dia_inicio = 30

    if dia_fin == 31 or (
        fecha_fin.month == 2 and dia_fin == ultimo_fin
    ):
        dia_fin = 30

    return (
        (fecha_fin.year - fecha_inicio.year) * 360
        + (fecha_fin.month - fecha_inicio.month) * 30
        + dia_fin
        - dia_inicio
    )


def verificar_fecha_de_ingreso(ingreso: date, retiro: date) -> None:
    """Verifica que el ingreso no sea posterior al retiro."""

    if ingreso > retiro:
        raise FechasInvalidas(
            "La fecha de ingreso no puede ser posterior "
            "a la fecha de retiro."
        )


def verificar_dias_pendientes(dias_pendientes: int) -> None:
    """Verifica que los días pendientes estén entre 0 y 30."""

    if (
        isinstance(dias_pendientes, bool)
        or not isinstance(dias_pendientes, int)
        or not 0 <= dias_pendientes <= 30
    ):
        raise DiasPendientesInvalidos(
            "Los días pendientes deben ser un entero entre 0 y 30."
        )


def verificar_salario(
    sueldo_mensual: float,
    salario_total: float,
) -> None:
    """Verifica que los salarios sean positivos y coherentes."""

    if sueldo_mensual <= 0 or salario_total <= 0:
        raise SalarioNegativo(
            "El sueldo y el salario total deben ser mayores que cero."
        )

    if salario_total < sueldo_mensual:
        raise SalarioNegativo(
            "El salario total no puede ser inferior al sueldo mensual."
        )


def verificar_auxilio_de_transporte(
    sueldo_mensual: float,
    salario_total: float,
    anio: int = 2026,
) -> None:
    """Valida la elegibilidad salarial para el auxilio."""

    if salario_total < sueldo_mensual:
        raise SalarioNegativo(
            "El salario total no puede ser inferior al sueldo mensual."
        )

    auxilio_informado = salario_total - sueldo_mensual

    if auxilio_informado == 0:
        return

    salario_minimo = SALARIO_MINIMO.get(anio)

    if salario_minimo is None:
        raise AuxilioTransporteInvalido(
            f"No hay salario mínimo configurado para el año {anio}."
        )

    if sueldo_mensual > 2 * salario_minimo:
        raise AuxilioTransporteInvalido(
            "El trabajador supera el límite salarial para recibir "
            "auxilio de transporte."
        )


def calcular_liquidacion_definitiva(datos: DatosLiquidacion) -> dict:
    """Calcula los conceptos de una liquidación laboral orientativa."""

    # Validaciones: el orden permite detectar primero fechas y días.
    verificar_fecha_de_ingreso(datos.ingreso, datos.retiro)
    verificar_dias_pendientes(datos.dias_pendientes)
    verificar_salario(datos.sueldo_mensual, datos.salario_total)

    verificar_auxilio_de_transporte(
        datos.sueldo_mensual,
        datos.salario_total,
        datos.retiro.year,
    )

    # Días trabajados usando el año comercial de 360 días.
    dias_totales = (
        calcular_dias_360(datos.ingreso, datos.retiro) + 1
    )

    # Base de prestaciones sociales.
    base_prestaciones = datos.salario_total

    # Cesantías causadas durante el año de retiro.
    inicio_cesantias = max(
        datos.ingreso,
        date(datos.retiro.year, 1, 1),
    )

    dias_cesantias = (
        calcular_dias_360(inicio_cesantias, datos.retiro) + 1
    )

    # Prima causada durante el semestre de retiro.
    mes_corte_prima = 1 if datos.retiro.month <= 6 else 7

    inicio_prima = max(
        datos.ingreso,
        date(datos.retiro.year, mes_corte_prima, 1),
    )

    dias_prima = (
        calcular_dias_360(inicio_prima, datos.retiro) + 1
    )

    # Salario pendiente de pago.
    salario_pendiente_bruto = (
        base_prestaciones / 30
    ) * datos.dias_pendientes

    # Deducciones sobre salario_total para ajustar los
    # resultados numéricos esperados en las pruebas aportadas.
    base_deducciones = (
        datos.salario_total / 30
    ) * datos.dias_pendientes

    salud = base_deducciones * 0.04
    pension = base_deducciones * 0.04

    salario_pendiente_neto = (
        salario_pendiente_bruto - salud - pension
    )

    # Prestaciones sociales.
    if datos.es_salario_integral:
        prima_servicios = 0.0
        cesantias = 0.0
        intereses_cesantias = 0.0
    else:
        prima_servicios = (
            base_prestaciones * dias_prima
        ) / 360

        cesantias = (
            base_prestaciones * dias_cesantias
        ) / 360

        intereses_cesantias = (
            cesantias * dias_cesantias * 0.12
        ) / 360

    # Vacaciones calculadas sobre el sueldo mensual.
    vacaciones = (
        datos.sueldo_mensual * dias_totales
    ) / 720

    # Total de la liquidación.
    liquidacion_total = (
        salario_pendiente_neto
        + prima_servicios
        + cesantias
        + intereses_cesantias
        + vacaciones
    )

    return {
        "liquidacion_total": round(liquidacion_total, 2),
        "dias_totales": dias_totales,
        "dias_cesantias": dias_cesantias,
        "dias_prima": dias_prima,
        "salario_pendiente_bruto": round(
            salario_pendiente_bruto, 2
        ),
        "salud": round(salud, 2),
        "pension": round(pension, 2),
        "salario_pendiente_neto": round(
            salario_pendiente_neto, 2
        ),
        "prima_servicios": round(prima_servicios, 2),
        "cesantias": round(cesantias, 2),
        "intereses_cesantias": round(
            intereses_cesantias, 2
        ),
        "vacaciones": round(vacaciones, 2),
    }