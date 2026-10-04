import sys
sys.path.append("src")

import unittest

from datetime import date
from model import logica_liquidacion_definitiva 
from model.logica_liquidacion_definitiva import CalculadoraLiquidacionDefinitiva

class TestsLiqDef ( unittest.TestCase):

    def test_caso_normal_1(self):

        calculadora = CalculadoraLiquidacionDefinitiva()
        resultado = calculadora.calcular(
        ingreso = date(2026, 1, 1),           # Año, Mes, Día
        retiro = date(2026, 12, 15),          # Año, Mes, Día
        sueldo_mensual = 1750905.0,           # Sin puntos ni comas
        sueldo_total = 2000000.0,            # Sueldo + Auxilio
        dias_pendientes = 15,
        es_salario_integral = False
    )

        
        print("--- RESULTADOS CASO NORMAL 1 (YASMIN URREGO) ---")
        
    
        for llave, valor in resultado.items():
            print(f"{llave}: ${valor:,.2f}")

    def test_caso_normal_2(self):
    
            calculadora = CalculadoraLiquidacionDefinitiva()
            resultado = calculadora.calcular(
            ingreso = date(2025, 3, 10),           # Año, Mes, Día
            retiro = date(2026, 8, 20),          # Año, Mes, Día
            sueldo_mensual = 1750905.0,           # Sin puntos ni comas
            sueldo_total = 2000000.0,            # Sueldo + Auxilio
            dias_pendientes = 0,
            es_salario_integral = False
        )
    
            print("--- RESULTADOS CASO NORMAL 2 (LAURA ECHEVERRY) ---")
            
        
            for llave, valor in resultado.items():
                print(f"{llave}: ${valor:,.2f}")

    def test_caso_normal_3(self):
        
            calculadora = CalculadoraLiquidacionDefinitiva()
            resultado = calculadora.calcular(
            ingreso = date(2026, 1, 1),           # Año, Mes, Día
            retiro = date(2026, 6, 30),          # Año, Mes, Día
            sueldo_mensual = 3950000.0,           # Sin puntos ni comas
            sueldo_total = 3950000.0,            # Sueldo + Auxilio
            dias_pendientes = 30,
            es_salario_integral = False
        )
        
           
            print("--- RESULTADOS CASO NORMAL 3 (DIEGO GOMEZ) ---")
                
           
            for llave, valor in resultado.items():
                print(f"{llave}: ${valor:,.2f}")

    def test_caso_extraordinario_1(self):
            
            calculadora = CalculadoraLiquidacionDefinitiva()
            resultado = calculadora.calcular(
            ingreso = date(2024, 5, 1),           # Año, Mes, Día
            retiro = date(2026, 10, 31),          # Año, Mes, Día
            sueldo_mensual = 1900000.0,           # Sin puntos ni comas
            sueldo_total = 2149095.0,            # Sueldo + Auxilio
            dias_pendientes = 0,
            es_salario_integral = False
        )
            
            
            print("--- RESULTADOS CASO EXTRAODINARIO 1 (NICOLAS OROZCO) ---")
                    
           
            for llave, valor in resultado.items():
                print(f"{llave}: ${valor:,.2f}")

    def test_caso_extraordinario_2(self):
            
            calculadora = CalculadoraLiquidacionDefinitiva()
            resultado = calculadora.calcular(
            ingreso = date(2026, 2, 1),           # Año, Mes, Día
            retiro = date(2026, 2, 28),          # Año, Mes, Día
            sueldo_mensual = 2000000.0,           # Sin puntos ni comas
            sueldo_total = 2249095.0,            # Sueldo + Auxilio
            dias_pendientes = 30,
            es_salario_integral = False
        )
            
            
            print("--- RESULTADOS CASO EXTRAODINARIO 2 (BRYAN MOSQUERA) ---")
                    
            
            for llave, valor in resultado.items():
                print(f"{llave}: ${valor:,.2f}")

    def test_caso_extraordinario_3(self):
            
            calculadora = CalculadoraLiquidacionDefinitiva()
            resultado = calculadora.calcular(
            ingreso = date(2025, 1, 1),           # Año, Mes, Día
            retiro = date(2026, 7, 30),          # Año, Mes, Día
            sueldo_mensual = 20000000.0,           # Sin puntos ni comas
            sueldo_total = 20000000.0,            # Sueldo + Auxilio
            dias_pendientes = 0,
            es_salario_integral = True
        )
            
            
            print("--- RESULTADOS CASO EXTRAODINARIO 3 (VALENTINA HIGUITA) ---")
                    
            
            for llave, valor in resultado.items():
                print(f"{llave}: ${valor:,.2f}")



    def test_error_1_fechas_invalidas(self):
        # Verifica que se genere la excepción FechasInvalidas adentro del bloque with
        calculadora = CalculadoraLiquidacionDefinitiva()
        with self.assertRaises(logica_liquidacion_definitiva.FechasInvalidas):
            calculadora.calcular(
                ingreso=date(2026, 9, 15),
                retiro=date(2026, 2, 28),
                sueldo_mensual=0,
                sueldo_total=0,
                dias_pendientes=0,
                es_salario_integral=False
            )

    def test_error_2_salario_negativo(self):
        calculadora = CalculadoraLiquidacionDefinitiva()
        with self.assertRaises(logica_liquidacion_definitiva.SalarioNegativo):
            calculadora.calcular(
                ingreso=date(2026, 2, 1),
                retiro=date(2026, 9, 25),
                sueldo_mensual=-2150000,
                sueldo_total=-2150000,
                dias_pendientes=25,
                es_salario_integral=False
            )

    def test_error_3_dias_pendientes_invalidos(self):
        calculadora = CalculadoraLiquidacionDefinitiva()
        with self.assertRaises(logica_liquidacion_definitiva.DiasPendientesInvalidos):
            calculadora.calcular(
                ingreso=date(2026, 1, 15),
                retiro=date(2026, 10, 31),
                sueldo_mensual=0,
                sueldo_total=0,
                dias_pendientes=35,
                es_salario_integral=False
            )

    def test_error_4_auxilio_de_transporte_invalido(self):
        calculadora = CalculadoraLiquidacionDefinitiva()
        with self.assertRaises(logica_liquidacion_definitiva.AuxilioTransporteInvalido):
            calculadora.calcular(
                ingreso=date(2025, 1, 10),
                retiro=date(2026, 12, 12),
                sueldo_mensual=18000000,
                sueldo_total=18249095,
                dias_pendientes=12,
                es_salario_integral=False
            )

if __name__ == '__main__':
    unittest.main()


        