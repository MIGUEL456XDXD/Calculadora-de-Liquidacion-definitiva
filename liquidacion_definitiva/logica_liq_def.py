from datetime import date

def calcular_dias_360(fecha_inicio: date, fecha_fin: date) -> int:
    """
    Helper: Calcula la diferencia de días usando el Año Comercial (Método Europeo).
    """
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
    sueldo_mensual: float,  # El salario pactado (Para deducir Salud/Pensión y Vacaciones)
    salario_total: float,   # Sueldo + Auxilio (Para pagar días pendientes, Prima y Cesantías)
    dias_pendientes: int,
    es_salario_integral: bool = False
) -> dict:
    """
    Motor matemático para calcular la liquidación definitiva.
    """
    # ==========================================
    # 1. CÁLCULO DE PERIODOS (DÍAS LABORADOS)
    # ==========================================
    dias_totales = calcular_dias_360(ingreso, retiro) + 1

    inicio_cesantias = max(ingreso, date(retiro.year, 1, 1))
    dias_cesantias = calcular_dias_360(inicio_cesantias, retiro) + 1

    mes_corte_prima = 1 if retiro.month <= 6 else 7
    inicio_prima = max(ingreso, date(retiro.year, mes_corte_prima, 1))
    dias_prima = calcular_dias_360(inicio_prima, retiro) + 1

    # ==========================================
    # 2. SALARIO PENDIENTE Y DEDUCCIONES
    # ==========================================
    # Se calcula el valor bruto a pagar usando el SALARIO TOTAL (que ya trae el auxilio)
    salario_pendiente_bruto = (salario_total / 30) * dias_pendientes
    
    # Las deducciones se calculan ESTRICTAMENTE sobre el SUELDO MENSUAL pactado
    base_deducciones = (sueldo_mensual / 30) * dias_pendientes
    salud = base_deducciones * 0.04
    pension = base_deducciones * 0.04
    
    salario_pendiente_neto = salario_pendiente_bruto - (salud + pension)

    # ==========================================
    # 3. PRESTACIONES SOCIALES
    # ==========================================
    if es_salario_integral:
        prima_servicios = 0.0
        cesantias = 0.0
        intereses_cesantias = 0.0
    else:
        # Se liquidan sobre el SALARIO TOTAL
        prima_servicios = (salario_total * dias_prima) / 360
        cesantias = (salario_total * dias_cesantias) / 360
        intereses_cesantias = (cesantias * dias_cesantias * 0.12) / 360

    # ==========================================
    # 4. VACACIONES
    # ==========================================
    # Se liquidan siempre sobre el SUELDO MENSUAL pactado
    vacaciones = (sueldo_mensual * dias_totales) / 720

    # ==========================================
    # 5. RETORNO DE RESULTADOS
    # ==========================================
    liquidacion_total = salario_pendiente_neto + prima_servicios + cesantias + intereses_cesantias + vacaciones

    return {
        "salario_pendiente": round(salario_pendiente_neto, 2),
        "salud": round(salud, 2),
        "pension": round(pension, 2),
        "prima_servicios": round(prima_servicios, 2),
        "cesantias": round(cesantias, 2),
        "intereses_cesantias": round(intereses_cesantias, 2),
        "vacaciones": round(vacaciones, 2),
        "liquidacion_total": round(liquidacion_total, 2)
    }