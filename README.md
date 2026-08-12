# Calculadora-de-Liquidacion-definitiva

Se requiere una aplicación que calcule el valor a pagar a un empleado que finaliza su contrato laboral con una empresa. Este proyecto automatiza el cálculo de la liquidación definitiva bajo la normativa laboral colombiana, garantizando precisión en el manejo de fechas, días comerciales y reglas de deducciones.

## 📥 Variables de Entrada

Para utilizar el motor de cálculo, la función principal recibe las siguientes variables (con sus nombres exactos en el código):

*   **`ingreso`** *(date)*: Fecha oficial de inicio del contrato laboral.
*   **`retiro`** *(date)*: Fecha oficial de finalización del contrato.
*   **`sueldo_mensual`** *(float)*: Salario base pactado en el contrato. Es crucial para el cálculo de vacaciones y para aplicar correctamente los descuentos de seguridad social (Salud y Pensión).
*   **`salario_total`** *(float)*: Es la suma del sueldo base más el auxilio de transporte (si aplica). Se utiliza como base prestacional para liquidar la Prima de Servicios y las Cesantías.
*   **`dias_pendientes`** *(int)*: Cantidad de días laborados en el último mes que la empresa aún le debe al trabajador (que no han sido pagados en una nómina regular).
*   **`es_salario_integral`** *(bool)*: Variable opcional que por defecto es `False`. Si se marca como `True` (para sueldos superiores a 13 SMMLV), el sistema aplica la regla de negocio omitiendo el cálculo de primas y cesantías.

## 📤 Variable de Salida

*   **`liquidacion_total`** *(float)*: El sistema retorna el valor neto final que la empresa debe consignarle o entregarle en cheque al trabajador tras sumar todos sus beneficios y restar las deducciones de ley. *(Nota: A nivel de código, la función retorna un diccionario detallado con el rubro de cada concepto, pero el monto definitivo a pagar se agrupa en esta llave).*

## ⚙️ ¿Qué calcula el código y cómo lo hace?

El motor matemático central realiza el cálculo en los siguientes pasos lógicos:

1.  **Cálculo de Días (Año Comercial):** El código utiliza el método europeo/comercial de 360 días anuales y 30 días mensuales. Aplica una regla donde los meses que terminan en 31 se ajustan matemáticamente a 30 para cumplir con la legislación laboral colombiana.
2.  **Salario Pendiente y Deducciones:** Calcula el dinero correspondiente a los `dias_pendientes` usando el `salario_total`. Sin embargo, separa el `sueldo_mensual` para calcular estrictamente sobre este último las deducciones de Ley (4% de Salud y 4% de Pensión), protegiendo así el auxilio de transporte de retenciones indebidas.
3.  **Prestaciones Sociales:**
    *   **Prima de Servicios:** Se calcula sobre el `salario_total` midiendo únicamente los días laborados en el semestre actual.
    *   **Cesantías:** Se calculan sobre el `salario_total` midiendo los días laborados desde el 1 de enero del año en curso (o desde el ingreso, si fue en el mismo año).
    *   **Intereses sobre Cesantías:** Equivalen al 12% anual sobre el saldo calculado de las cesantías.
4.  **Vacaciones:** Al no ser una prestación social sino un descanso remunerado, se calculan utilizando el total histórico de días trabajados en toda la vigencia del contrato, pero multiplicados estrictamente por el `sueldo_mensual` pactado.
5.  **Validación de Salario Integral:** Si el trabajador goza de salario integral, el motor internamente ajusta a $0 la prima, las cesantías y sus intereses, liquidando únicamente las vacaciones acumuladas y el salario pendiente.
