import unittest
from datetime import date
import logica_liq_def 

class TestsLiqDef ( unittest.TestCase):

    def test_normal_1(self):

        resultado = logica_liq_def.calcular_liquidacion_definitiva(
        ingreso = date(2026, 1, 1),           # Año, Mes, Día
        retiro = date(2026, 12, 15),          # Año, Mes, Día
        sueldo_mensual = 1750905.0,           # Sin puntos ni comas
        salario_total = 2000000.0,            # Sueldo + Auxilio
        dias_pendientes = 15,
        es_salario_integral = False
    )

        
        print("--- RESULTADOS CASO NORMAL 1 (YASMIN URREGO) ---")
        
    
        for llave, valor in resultado.items():
            print(f"{llave}: ${valor:,.2f}")

    def test_normal_2(self):
    
            resultado = logica_liq_def.calcular_liquidacion_definitiva(
            ingreso = date(2025, 3, 10),           # Año, Mes, Día
            retiro = date(2026, 8, 20),          # Año, Mes, Día
            sueldo_mensual = 1750905.0,           # Sin puntos ni comas
            salario_total = 2000000.0,            # Sueldo + Auxilio
            dias_pendientes = 0,
            es_salario_integral = False
        )
    
            print("--- RESULTADOS CASO NORMAL 2 (LAURA ECHEVERRY) ---")
            
        
            for llave, valor in resultado.items():
                print(f"{llave}: ${valor:,.2f}")

    def test_normal_3(self):
        
            resultado = logica_liq_def.calcular_liquidacion_definitiva(
            ingreso = date(2026, 1, 1),           # Año, Mes, Día
            retiro = date(2026, 6, 30),          # Año, Mes, Día
            sueldo_mensual = 3950000.0,           # Sin puntos ni comas
            salario_total = 3950000.0,            # Sueldo + Auxilio
            dias_pendientes = 30,
            es_salario_integral = False
        )
        
           
            print("--- RESULTADOS CASO NORMAL 3 (DIEGO GOMEZ) ---")
                
           
            for llave, valor in resultado.items():
                print(f"{llave}: ${valor:,.2f}")

    def test_extraordinario_1(self):
            
            resultado = logica_liq_def.calcular_liquidacion_definitiva(
            ingreso = date(2024, 5, 1),           # Año, Mes, Día
            retiro = date(2026, 10, 31),          # Año, Mes, Día
            sueldo_mensual = 1900000.0,           # Sin puntos ni comas
            salario_total = 2149095.0,            # Sueldo + Auxilio
            dias_pendientes = 0,
            es_salario_integral = False
        )
            
            
            print("--- RESULTADOS CASO EXTRAODINARIO 1 (NICOLAS OROZCO) ---")
                    
           
            for llave, valor in resultado.items():
                print(f"{llave}: ${valor:,.2f}")

    def test_extraordinario_2(self):
            
            resultado = logica_liq_def.calcular_liquidacion_definitiva(
            ingreso = date(2026, 2, 1),           # Año, Mes, Día
            retiro = date(2026, 2, 28),          # Año, Mes, Día
            sueldo_mensual = 2000000.0,           # Sin puntos ni comas
            salario_total = 2249095.0,            # Sueldo + Auxilio
            dias_pendientes = 30,
            es_salario_integral = False
        )
            
            
            print("--- RESULTADOS CASO EXTRAODINARIO 2 (BRYAN MOSQUERA) ---")
                    
            
            for llave, valor in resultado.items():
                print(f"{llave}: ${valor:,.2f}")

    def test_extraordinario_3(self):
            
            resultado = logica_liq_def.calcular_liquidacion_definitiva(
            ingreso = date(2025, 1, 1),           # Año, Mes, Día
            retiro = date(2026, 7, 30),          # Año, Mes, Día
            sueldo_mensual = 20000000.0,           # Sin puntos ni comas
            salario_total = 20000000.0,            # Sueldo + Auxilio
            dias_pendientes = 0,
            es_salario_integral = True
        )
            
            
            print("--- RESULTADOS CASO EXTRAODINARIO 3 (VALENTINA HIGUITA) ---")
                    
            
            for llave, valor in resultado.items():
                print(f"{llave}: ${valor:,.2f}")



    def test_error_1_fechas(self):
        # Verifica que se genere la excepción FechasInvalidas adentro del bloque with
        with self.assertRaises(logica_liq_def.FechasInvalidas):
            logica_liq_def.calcular_liquidacion_definitiva(
                ingreso=date(2026, 9, 15),
                retiro=date(2026, 2, 28),
                sueldo_mensual=0,
                salario_total=0,
                dias_pendientes=0
            )

    def test_error_2_salario(self):
        with self.assertRaises(logica_liq_def.SalarioNegativo):
            logica_liq_def.calcular_liquidacion_definitiva(
                ingreso=date(2026, 2, 1),
                retiro=date(2026, 9, 25),
                sueldo_mensual=-2150000,
                salario_total=-2150000,
                dias_pendientes=25
            )

    def test_error_3_dias(self):
        with self.assertRaises(logica_liq_def.DiasPendientesInvalidos):
            logica_liq_def.calcular_liquidacion_definitiva(
                ingreso=date(2026, 1, 15),
                retiro=date(2026, 10, 31),
                sueldo_mensual=0,
                salario_total=0,
                dias_pendientes=35
            )

    def test_error_4_auxilio(self):
        with self.assertRaises(logica_liq_def.AuxilioTransporteInvalido):
            logica_liq_def.calcular_liquidacion_definitiva(
                ingreso=date(2025, 1, 10),
                retiro=date(2026, 12, 12),
                sueldo_mensual=18000000,
                salario_total=18249095,
                dias_pendientes=12
            )

if __name__ == '__main__':
    unittest.main()


        