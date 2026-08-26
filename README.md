
# Calculadora-de-Liquidacion-definitiva

Se requiere una aplicación que calcule el valor a pagar a un empleado que finaliza su contrato laboral con una empresa. Este proyecto automatiza el cálculo de la liquidación definitiva bajo la normativa laboral colombiana, garantizando precisión en el manejo de fechas, días comerciales y reglas de deducciones.

##  Integrantes del proyecto
*Hans Schoonewolff Otero*

*Miguel Obando Serna*

## Arquitectura del Proyecto

Este proyecto está construido siguiendo los principios de separación de responsabilidades, basándose en la arquitectura **MVC (Modelo-Vista-Controlador)**. 

La estructura del repositorio divide de forma estricta la lógica matemática de la interfaz de usuario. Esto garantiza que el código sea escalable, fácil de mantener y que se puedan crear nuevas interfaces (como aplicaciones web o gráficas) en el futuro sin necesidad de alterar los cálculos base.

La organización del proyecto es la siguiente:

### 1. `src/model/` (El Modelo)
* **Archivo principal:** `logica_liq_def.py`
* **Responsabilidad:** Es el núcleo del sistema. Aquí residen todas las reglas de negocio, las fórmulas correspondientes a la legislación laboral colombiana (cesantías, intereses, vacaciones) y la validación de excepciones.
* **Restricciones:** Este módulo funciona de manera aislada; no contiene instrucciones de consola (`print` o `input`). Únicamente recibe datos, procesa cálculos y retorna un diccionario de resultados o lanza errores controlados (`raise`).

### 2. `src/view/console/` (La Vista)
* **Archivo principal:** `consola_usuario.py`
* **Responsabilidad:** Se encarga de la interacción directa con la persona que utiliza el software. 
* **Flujo:** Captura los datos a través de la terminal, invoca las funciones del **Modelo** enviando la información, y formatea la respuesta para mostrar los valores monetarios en pantalla de forma amigable. Además, captura los errores generados por el modelo (`try/except`) para mostrar mensajes claros sin que el programa colapse.

### 3. `tests/` (Pruebas Unitarias)
* **Archivo principal:** `tests_liq_def.py`
* **Responsabilidad:** Asegurar la calidad y precisión del software. Utiliza la librería `unittest` nativa de Python para evaluar la calculadora de liquidación bajo múltiples escenarios (casos de éxito normales, casos de error por violaciones a las reglas de negocio, y casos extraordinarios), garantizando que las futuras modificaciones en el código no rompan la lógica existente.

### Comando para ejecutar las pruebas unitarias

Para verificar que todos los cálculos matemáticos de la liquidación y las reglas de negocio funcionan correctamente, abre la terminal en la carpeta raíz del proyecto y ejecuta el siguiente comando:

```bash
python -m unittest tests/tests_liq_def.py

### Comando para ejecutar la aplicación (Interfaz de Consola)

Para iniciar la calculadora de liquidación y comenzar a interactuar con el programa, abre la terminal asegurándote de estar en la carpeta raíz del proyecto y ejecuta el siguiente comando:

```bash
python src/view/consola_usuario.py

## 📥 Variables de Entrada

Para utilizar el motor de cálculo, la función principal recibe las siguientes variables:

*   **`ingreso`** *(date)*: Fecha oficial de inicio del contrato laboral.
*   **`retiro`** *(date)*: Fecha oficial de finalización del contrato.
*   **`sueldo_mensual`** *(float)*: Salario base pactado en el contrato. Es crucial para el cálculo de vacaciones y para aplicar correctamente los descuentos de seguridad social (Salud y Pensión).
*   **`salario_total`** *(float)*: Es la suma del sueldo base más el auxilio de transporte (si aplica). Se utiliza como base prestacional para liquidar la Prima de Servicios y las Cesantías.
*   **`dias_pendientes`** *(int)*: Cantidad de días laborados en el último mes que la empresa aún le debe al trabajador.
*   **`es_salario_integral`** *(bool)*: Variable opcional (`False` por defecto). Si es `True` (para sueldos superiores a 13 SMMLV), el sistema aplica la regla de negocio omitiendo el cálculo de primas y cesantías.

## 📤 Variables de Salida

Al ejecutarse, el sistema retorna un diccionario estructurado con el desglose exacto de cada concepto, entregando las siguientes variables de salida:

*   **`dias_laborados`** *(int)*: Total histórico de días trabajados bajo el sistema de año comercial.
*   **`salario_pendiente`** *(float)*: Valor neto a pagar por los días del último mes (ya con deducciones aplicadas).
*   **`salud`** *(float)*: Deducción legal del 4% calculada estrictamente sobre la proporción del `sueldo_mensual`.
*   **`pension`** *(float)*: Deducción legal del 4% calculada estrictamente sobre la proporción del `sueldo_mensual`.
*   **`prima_servicios`** *(float)*: Compensación semestral calculada sobre el `salario_total` por los días laborados en el semestre de retiro.
*   **`cesantias`** *(float)*: Auxilio proporcional calculado sobre el `salario_total` desde el 1 de enero del año en curso (o desde el ingreso).
*   **`intereses_cesantias`** *(float)*: Rentabilidad legal del 12% anual sobre el saldo acumulado de las cesantías.
*   **`vacaciones`** *(float)*: Descanso remunerado compensado en dinero, calculado históricamente sobre el `sueldo_mensual`.
*   **`liquidacion_total`** *(float)*: La suma definitiva y neta de todos los rubros a favor del trabajador.

## ⚙️ ¿Qué calcula el código y cómo lo hace?

El motor matemático central realiza el cálculo en los siguientes pasos lógicos:

1.  **Cálculo de Días (Año Comercial):** El código utiliza el método europeo/comercial de 360 días anuales y 30 días mensuales. Aplica una regla donde los meses que terminan en 31 se ajustan matemáticamente a 30 para cumplir con la legislación laboral colombiana.
2.  **Salario Pendiente y Deducciones:** Calcula el ingreso bruto correspondiente a los `dias_pendientes` usando el `salario_total`. Sin embargo, separa el `sueldo_mensual` para calcular estrictamente sobre este último las deducciones de Ley (4% de Salud y 4% de Pensión), protegiendo así el auxilio de transporte de retenciones indebidas.
3.  **Prestaciones Sociales:**
    *   **Prima de Servicios:** Se calcula sobre el `salario_total` midiendo únicamente los días laborados en el semestre actual.
    *   **Cesantías:** Se calculan sobre el `salario_total` midiendo los días laborados en el año en curso.
    *   **Intereses sobre Cesantías:** Equivalen al 12% anual sobre el saldo de las cesantías.
4.  **Vacaciones:** Al no ser una prestación social sino un descanso remunerado, se calculan utilizando el total histórico de días trabajados en toda la vigencia del contrato, pero multiplicados estrictamente por el `sueldo_mensual` pactado.
5.  **Validación de Salario Integral:** Si el trabajador goza de salario integral, el motor internamente ajusta a $0 la prima, las cesantías y sus intereses, liquidando únicamente las vacaciones acumuladas y el salario del último mes.
