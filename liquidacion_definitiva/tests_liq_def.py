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

        # 3. VERIFICAR EL RESULTADO (Assert / Print)
        print("--- RESULTADOS CASO NORMAL 1 (YASMIN URREGO) ---")
        
        # Imprimimos el diccionario resultante línea por línea para que se vea ordenado
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
    
            # 3. VERIFICAR EL RESULTADO (Assert / Print)
            print("--- RESULTADOS CASO NORMAL 2 (LAURA ECHEVERRY) ---")
            
            # Imprimimos el diccionario resultante línea por línea para que se vea ordenado
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
        
            # 3. VERIFICAR EL RESULTADO (Assert / Print)
            print("--- RESULTADOS CASO NORMAL 2 (DIEGO GOMEZ) ---")
                
            # Imprimimos el diccionario resultante línea por línea para que se vea ordenado
            for llave, valor in resultado.items():
                print(f"{llave}: ${valor:,.2f}")



if __name__ == '__main__':
    unittest.main()


        