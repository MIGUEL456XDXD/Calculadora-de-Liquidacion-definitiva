import unittest
from datetime import date
from logica_liq_def import calcular_liquidacion_definitiva

class TestsLiqDef ( unittest.TestCase):

    def test_normal_1(self):

        resultado = calcular_liquidacion_definitiva(
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
    
            resultado = calcular_liquidacion_definitiva(
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
        
            resultado = calcular_liquidacion_definitiva(
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
            
            resultado = calcular_liquidacion_definitiva(
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
            
            resultado = calcular_liquidacion_definitiva(
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
            
            resultado = calcular_liquidacion_definitiva(
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




if __name__ == '__main__':
    unittest.main()
