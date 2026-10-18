
"""Pruebas unitarias para la liquidación definitiva."""

import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from model import logica_liquidacion_definitiva as logica


class TestsLiqDef(unittest.TestCase):
    """Pruebas de los casos normales, extraordinarios y de error."""

    def calcular(
        self,
        ingreso,
        retiro,
        sueldo_mensual,
        salario_total,
        dias_pendientes,
        es_salario_integral=False,
    ):
        datos = logica.DatosLiquidacion(
            ingreso=ingreso,
            retiro=retiro,
            sueldo_mensual=sueldo_mensual,
            salario_total=salario_total,
            dias_pendientes=dias_pendientes,
            es_salario_integral=es_salario_integral,
        )
        return logica.calcular_liquidacion_definitiva(datos)

    def comprobar_total(self, resultado, esperado):
        self.assertAlmostEqual(
            resultado["liquidacion_total"],
            esperado,
            places=2,
        )

    # 1. CASO NORMAL 1

    def test_normal_1(self):
        resultado = self.calcular(
            date(2026, 1, 1),
            date(2026, 12, 15),
            1750905,
            2000000,
            15,
        )
        self.comprobar_total(resultado, 4812725.31)

    # 2. CASO NORMAL 2

    def test_normal_2(self):
        resultado = self.calcular(
            date(2025, 3, 10),
            date(2026, 8, 20),
            1750905,
            2000000,
            0,
        )
        self.comprobar_total(resultado, 2920492.83)

    # 3. CASO NORMAL 3

    def test_normal_3(self):
        resultado = self.calcular(
            date(2026, 1, 1),
            date(2026, 6, 30),
            3950000,
            3950000,
            30,
        )
        self.comprobar_total(resultado, 8690000.00)

    # 4. CASO EXTRAORDINARIO 1

    def test_extraordinario_1(self):
        resultado = self.calcular(
            date(2024, 5, 1),
            date(2026, 10, 31),
            1900000,
            2149095,
            0,
        )
        self.comprobar_total(resultado, 5061368.75)

    # 5. CASO EXTRAORDINARIO 2

    def test_extraordinario_2(self):
        resultado = self.calcular(
            date(2026, 2, 1),
            date(2026, 2, 28),
            2000000,
            2249095,
            30,
        )
        self.comprobar_total(resultado, 2529224.15)

    # 6. CASO EXTRAORDINARIO 3: SALARIO INTEGRAL

    def test_extraordinario_3_salario_integral(self):
        resultado = self.calcular(
            date(2025, 1, 1),
            date(2026, 7, 30),
            20000000,
            20000000,
            0,
            es_salario_integral=True,
        )
        self.comprobar_total(resultado, 15833333.33)

    # 7. ERROR: FECHA DE INGRESO POSTERIOR AL RETIRO

    def test_error_1_fechas(self):
        with self.assertRaises(logica.FechasInvalidas):
            self.calcular(
                date(2026, 9, 15),
                date(2026, 2, 28),
                0,
                0,
                0,
            )

    # 8. ERROR: SALARIO NEGATIVO

    def test_error_2_salario(self):
        with self.assertRaises(logica.SalarioNegativo):
            self.calcular(
                date(2026, 2, 1),
                date(2026, 9, 25),
                -2150000,
                -2150000,
                25,
            )

    # 9. ERROR: MÁS DE 30 DÍAS PENDIENTES

    def test_error_3_dias(self):
        with self.assertRaises(logica.DiasPendientesInvalidos):
            self.calcular(
                date(2026, 1, 15),
                date(2026, 10, 31),
                0,
                0,
                35,
            )

    # 10. ERROR: AUXILIO DE TRANSPORTE NO PERMITIDO

    def test_error_4_auxilio(self):
        with self.assertRaises(logica.AuxilioTransporteInvalido):
            self.calcular(
                date(2025, 1, 10),
                date(2026, 12, 12),
                18000000,
                18249095,
                12,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)