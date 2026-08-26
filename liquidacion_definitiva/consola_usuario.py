from datetime import date
from logica_liq_def import calcular_liquidacion_definitiva

print("--- CALCULADORA DE LIQUIDACIÓN ---")

# 1. Pedir fecha de ingreso
print("Ingresa la fecha de INGRESO:")
dia_ing = int(input("Día: "))
mes_ing = int(input("Mes: "))
ano_ing = int(input("Año: "))
fecha_ingreso = date(ano_ing, mes_ing, dia_ing)

# 2. Pedir fecha de retiro
print("\nIngresa la fecha de RETIRO:")
dia_ret = int(input("Día: "))
mes_ret = int(input("Mes: "))
ano_ret = int(input("Año: "))
fecha_retiro = date(ano_ret, mes_ret, dia_ret)

# 3. Pedir datos de dinero y tiempo
print("\nIngresa los datos del salario:")
sueldo_mensual = float(input("Sueldo mensual pactado (ej. 1750905): "))
aux_transporte = float(input("Auxilio de transporte (0 si no aplica): "))
salario_total = sueldo_mensual + aux_transporte

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

# Revisiones de error
if "error" in resultado:
    print(resultado["error"])
else:
    for llave, valor in resultado.items():
        print(f"{llave}: {valor}")
