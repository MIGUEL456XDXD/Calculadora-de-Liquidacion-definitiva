from datetime import date


# clases de exepciones

class FechasInvalidas(Exception):
    """ Se dispara cuando la fecha de ingreso es posterior al retiro """

class SalarioNegativo(Exception):
    """ Se dispara cuando el sueldo o salario total es menor a cero """

class DiasPendientesInvalidos(Exception):
    """ Se dispara cuando los días pendientes son menores a 0 o mayores a 30 """

class AuxilioTransporteInvalido(Exception):
    """ Se dispara cuando el sueldo supera el tope pero se cobra auxilio """


# Calculo matematico

def calcular_dias_360(fecha_inicio: date, fecha_fin: date) -> int:
    """ Helper: Calcula la diferencia de días usando el Año Comercial. """
    d1, m1, y1 = fecha_inicio.day, fecha_inicio.month, fecha_inicio.year
    d2, m2, y2 = fecha_fin.day, fecha_fin.month, fecha_fin.year
    
    if d1 == 31: d1 = 30
    if d2 == 31: d2 = 30
    if d1 == 28: d1 = 30
    if d2 == 28: d2 = 30
        
    return (y2 - y1) * 360 + (m2 - m1) * 30 + (d2 - d1)


def calcular_liquidacion_definitiva(
    ingreso: date,
    retiro: date,
    sueldo_mensual: float,  
    salario_total: float,   
    dias_pendientes: int,
    es_salario_integral: bool = False
) -> dict:

    # 1. Validaciones
    if ingreso > retiro:
        raise FechasInvalidas("La fecha de ingreso no puede ser posterior a la fecha de retiro.")

    if sueldo_mensual < 0 or salario_total < 0:
        raise SalarioNegativo("El salario no puede ser negativo.")

    if dias_pendientes < 0 or dias_pendientes > 30:
        raise DiasPendientesInvalidos("Los días pendientes no pueden superar los 30 días.")

    limite_auxilio = 3501810
    if sueldo_mensual > limite_auxilio and salario_total > sueldo_mensual:
        raise AuxilioTransporteInvalido("El trabajador no tiene derecho al auxilio de transporte.")

    # 2. Logica de la liquidacion definitva
    dias_totales = calcular_dias_360(ingreso, retiro) + 1

    inicio_cesantias = max(ingreso, date(retiro.year, 1, 1))
    dias_cesantias = calcular_dias_360(inicio_cesantias, retiro) + 1

    mes_corte_prima = 1 if retiro.month <= 6 else 7
    inicio_prima = max(ingreso, date(retiro.year, mes_corte_prima, 1))
    dias_prima = calcular_dias_360(inicio_prima, retiro) + 1

    salario_pendiente_bruto = (salario_total / 30) * dias_pendientes
    
    base_deducciones = (salario_total / 30) * dias_pendientes 
    salud = base_deducciones * 0.04
    pension = base_deducciones * 0.04
    
    salario_pendiente_neto = salario_pendiente_bruto - (salud + pension)

    if es_salario_integral:
        prima_servicios = 0.0
        cesantias = 0.0
        intereses_cesantias = 0.0
    else:
        prima_servicios = (salario_total * dias_prima) / 360
        cesantias = (salario_total * dias_cesantias) / 360
        intereses_cesantias = (cesantias * dias_cesantias * 0.12) / 360

    vacaciones = (sueldo_mensual * dias_totales) / 720

    liquidacion_total = salario_pendiente_neto + prima_servicios + cesantias + intereses_cesantias + vacaciones

    # 3. RETORNO DE RESULTADOS 
    return {
        
        "liquidacion_total": round(liquidacion_total, 2)
    }

""" 
        "dias_cesantias": dias_cesantias,
        "base_deducciones": base_deducciones,
        "dias_pendientes": dias_pendientes,
        "dias_prima": dias_prima,
        "dias_laborados": dias_totales,
        "salario_pendiente": round(salario_pendiente_bruto, 2),
        "salud": round(salud, 2),
        "pension": round(pension, 2),
        "prima_servicios": round(prima_servicios, 2),
        "cesantias": round(cesantias, 2),
        "intereses_cesantias": round(intereses_cesantias, 2),
        "vacaciones": round(vacaciones, 2),
        """
