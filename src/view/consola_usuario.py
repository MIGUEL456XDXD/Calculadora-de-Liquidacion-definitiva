import sys
sys.path.append("src")

from datetime import date
from model import logica_liquidacion_definitiva
from model.logica_liquidacion_definitiva import calcular_liquidacion_definitiva

print("--- CALCULADORA DE LIQUIDACIÓN ---")

# 1. Pedir fecha de ingreso por partes
print("Ingresa la fecha de INGRESO:")
dia_ingreso = int(input("Día: "))
mes_ingreso = int(input("Mes: "))
ano_ingreso = int(input("Año: "))
fecha_ingreso = date(ano_ingreso, mes_ingreso, dia_ingreso)

# 2. Pedir fecha de retiro por partes
print("\nIngresa la fecha de RETIRO:")
dia_retiro = int(input("Día: "))
mes_retiro = int(input("Mes: "))
ano_retiro = int(input("Año: "))
fecha_retiro = date(ano_retiro, mes_retiro, dia_retiro)

# 3. Pedir datos de dinero y tiempo
print("\nIngresa los datos del salario:")
sueldo_mensual = float(input("Sueldo mensual pactado (ej. 1750905): "))
auxilio_transporte = float(input("Auxilio de transporte (0 si no aplica): "))
salario_total = sueldo_mensual + auxilio_transporte

dias_pendientes = int(input("Días pendientes de pago del último mes: "))

# 4. Preguntar si es salario integral
respuesta = input("¿El empleado tiene salario integral? (si/no): ")
if respuesta.lower() == "si":
    es_salario_integral = True
else:
    es_salario_integral = False

# 5. Llamar a la función principal
resultado = calcular_liquidacion_definitiva(
    ingreso=fecha_ingreso,
    retiro=fecha_retiro,
    sueldo_mensual=sueldo_mensual,
    salario_total=salario_total,
    dias_pendientes=dias_pendientes,
    es_salario_integral=es_salario_integral
)

# 6. Mostrar los resultados
print("\n=== RESULTADOS DE LA LIQUIDACIÓN ===")

# Revisamos si la función devolvió algún error
if "error" in resultado:
    print(resultado["error"])
else:
    # Si todo salió bien, imprimimos los datos uno por uno
    for llave, valor in resultado.items():
        print(f"{llave}: {valor}")