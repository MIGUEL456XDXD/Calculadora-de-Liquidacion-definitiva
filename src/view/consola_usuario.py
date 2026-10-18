
"""Interfaz de consola para la calculadora de liquidación definitiva."""

import sys
from pathlib import Path
from datetime import date
from decimal import Decimal, InvalidOperation

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.model import logica_liquidacion_definitiva as logica
from src.controller import liquidacion_controller as controlador


def solicitar_fecha(mensaje: str) -> date:
    while True:
        print(mensaje)
        try:
            dia = int(input("Día: "))
            mes = int(input("Mes: "))
            ano = int(input("Año: "))
            return date(ano, mes, dia)
        except ValueError:
            print("Fecha inválida. Intenta de nuevo.")


def solicitar_float(mensaje: str) -> float:
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("Ingresa un número válido.")


def calcular_liquidacion() -> None:
    print("\n--- CALCULAR LIQUIDACIÓN ---")
    try:
        ingreso = solicitar_fecha("Fecha de ingreso:")
        retiro = solicitar_fecha("Fecha de retiro:")

        sueldo = solicitar_float("Sueldo mensual: ")
        auxilio = solicitar_float("Auxilio de transporte (0 si no aplica): ")
        dias = int(input("Días pendientes de pago del último mes: "))

        respuesta = input("¿Tiene salario integral? (si/no): ").strip().lower()
        while respuesta not in ("si", "sí", "no"):
            respuesta = input("Responde si o no: ").strip().lower()

        datos = logica.DatosLiquidacion(
            ingreso=ingreso,
            retiro=retiro,
            sueldo_mensual=sueldo,
            salario_total=sueldo + auxilio,
            dias_pendientes=dias,
            es_salario_integral=respuesta in ("si", "sí"),
        )

        resultado = logica.calcular_liquidacion_definitiva(datos)
        print("\n=== RESULTADOS ===")
        for llave, valor in resultado.items():
            print(f"{llave}: {valor}")

    except (
        ValueError,
        logica.FechasInvalidas,
        logica.SalarioNegativo,
        logica.DiasPendientesInvalidos,
        logica.AuxilioTransporteInvalido,
    ) as error:
        print(f"Error: {error}")


def guardar_liquidacion() -> None:
    print("\n--- GUARDAR LIQUIDACIÓN ---")
    try:
        ingreso = solicitar_fecha("Fecha de ingreso:")
        retiro = solicitar_fecha("Fecha de retiro:")

        while True:
            try:
                salario = Decimal(input("Salario mensual: "))
                break
            except InvalidOperation:
                print("Ingresa un salario válido.")

        dias = int(input("Días trabajados: "))
        respuesta = input("¿Tiene salario integral? (si/no): ").strip().lower()
        while respuesta not in ("si", "sí", "no"):
            respuesta = input("Responde si o no: ").strip().lower()

        identificador = controlador.insertar_liquidacion(
            fecha_ingreso=ingreso,
            fecha_retiro=retiro,
            salario=salario,
            dias_trabajados=dias,
            salario_integral=respuesta in ("si", "sí"),
        )
        print(f"Liquidación guardada. ID: {identificador}")

    except (ValueError, InvalidOperation) as error:
        print(f"Datos inválidos: {error}")
    except Exception as error:
        print(f"No se pudo guardar la liquidación: {error}")


def buscar_liquidacion() -> None:
    print("\n--- BUSCAR LIQUIDACIÓN ---")
    try:
        identificador = int(input("ID de la liquidación: "))
        liquidacion = controlador.buscar_liquidacion(identificador)

        if liquidacion is None:
            print("No se encontró una liquidación con ese ID.")
            return

        print(f"ID: {liquidacion.id}")
        print(f"Fecha de ingreso: {liquidacion.fecha_ingreso}")
        print(f"Fecha de retiro: {liquidacion.fecha_retiro}")
        print(f"Salario: {liquidacion.salario}")
        print(f"Días trabajados: {liquidacion.dias_trabajados}")
        print(f"Salario integral: {liquidacion.salario_integral}")

    except ValueError:
        print("El ID debe ser un número entero.")
    except Exception as error:
        print(f"No se pudo consultar la base de datos: {error}")


def ejecutar_calculadora() -> None:
    while True:
        print("\n=== CALCULADORA DE LIQUIDACIÓN ===")
        print("1. Calcular liquidación")
        print("2. Guardar liquidación")
        print("3. Buscar liquidación por ID")
        print("4. Salir")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            calcular_liquidacion()
        elif opcion == "2":
            guardar_liquidacion()
        elif opcion == "3":
            buscar_liquidacion()
        elif opcion == "4":
            print("Hasta luego.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    ejecutar_calculadora()
