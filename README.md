
# Calculadora de Liquidación Definitiva

## 1. Descripción del proyecto

Este proyecto consiste en una calculadora de liquidación definitiva desarrollada en Python. La aplicación permite realizar cálculos laborales desde una interfaz de consola y guardar los datos en una base de datos PostgreSQL para consultarlos posteriormente.

Durante el desarrollo trabajamos en la lógica de los cálculos, la conexión con PostgreSQL, el modelo ORM, las operaciones de inserción, consulta y eliminación, y las pruebas automatizadas.

La idea es que la información no se quede solamente en pantalla, sino que también quede registrada en la base de datos.

## 2. Integrantes

- Hans
- Miguel Obando

## 3. Funcionalidades implementadas

La aplicación cuenta con las siguientes opciones:

1. Calcular una liquidación definitiva.
2. Guardar una liquidación en PostgreSQL.
3. Buscar una liquidación por su ID.
4. Crear las tablas necesarias.
5. Eliminar las tablas mediante la funcionalidad del controlador.
6. Validar los datos ingresados.
7. Ejecutar pruebas automatizadas con Pytest.

En los cálculos se manejan conceptos como salario pendiente, salud, pensión, prima de servicios, cesantías, intereses a las cesantías y vacaciones, de acuerdo con la lógica implementada en el proyecto.

## 4. Tecnologías utilizadas

- Python 3.14
- PostgreSQL 17
- SQLAlchemy: conexión y mapeo ORM
- Psycopg: comunicación con PostgreSQL
- Pytest: pruebas automatizadas
- Visual Studio Code: entorno de desarrollo

## 5. Estructura del proyecto

```text
Calculadora-de-Liquidacion-definitiva/
│
├── README.md
├── .gitignore
├── secret_config_sample.py
│
├── doc/
├── .vscode/
│
├── src/
│   ├── controller/
│   │   └── liquidacion_controller.py
│   │
│   ├── database/
│   │   └── conexion.py
│   │
│   ├── model/
│   │   ├── __init__.py
│   │   ├── logica_liquidacion_definitiva.py
│   │   └── modelo_liquidacion.py
│   │
│   └── view/
│       ├── __init__.py
│       └── consola_usuario.py
│
└── tests/
    ├── test_controller_liquidacion.py
    └── test_liq_def.py
```

### Organización del código

- **Model:** contiene la lógica de liquidación y el modelo ORM que representa la tabla de la base de datos.
- **Controller:** contiene las operaciones para guardar, buscar y eliminar registros, además de crear y borrar las tablas.
- **Database:** configura la conexión con PostgreSQL y la sesión de SQLAlchemy.
- **View:** contiene el menú de consola y la interacción con el usuario.
- **Tests:** contiene las pruebas de las operaciones del controlador y de los cálculos.

## 6. Requisitos previos

Antes de ejecutar el proyecto, se necesita tener instalado:

- Python 3.14.
- PostgreSQL 17.
- Las librerías utilizadas por el código del proyecto.

Los siguientes comandos están preparados para Windows y PowerShell, usando la ubicación del proyecto durante el desarrollo.

## 7. Abrir el proyecto en PowerShell

Primero, entrar a la carpeta del proyecto:

```powershell
Set-Location "C:\Users\USUARIO\.vscode\Calculadora-de-Liquidacion-definitiva"
```

Comprobar que se encuentran los archivos:

```powershell
Get-ChildItem
```

## 8. Comprobar el servicio de PostgreSQL

Verificar que el servicio de PostgreSQL 17 esté iniciado:

```powershell
Get-Service -Name "postgresql-x64-17"
```

El estado esperado es:

```text
Status : Running
```

Después, comprobar que el puerto de PostgreSQL responda:

```powershell
Test-NetConnection localhost -Port 5432
```

La conexión TCP se considera disponible cuando aparece:

```text
TcpTestSucceeded : True
```

## 9. Crear la base de datos

La base de datos utilizada por la aplicación se llama `liquidaciones_db` y el usuario utilizado durante las pruebas de conexión fue `postgres`.

Si la base de datos todavía no existe, se puede crear con:

```powershell
& "C:\Program Files\PostgreSQL\17\bin\createdb.exe" -U postgres liquidaciones_db
```

Si ya existe, no es necesario volver a crearla.

Para comprobar la conexión y confirmar el nombre de la base de datos:

```powershell
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d liquidaciones_db -c "SELECT current_database(), current_user;"
```

El resultado debe mostrar `liquidaciones_db` como base de datos y `postgres` como usuario si se utiliza esa misma configuración.

### Contraseña de PostgreSQL

Cuando PostgreSQL solicita la contraseña en PowerShell, los caracteres no se muestran mientras se escriben. Es normal: se escribe la contraseña y se presiona Enter.

No es necesario que aparezcan asteriscos ni puntos.

## 10. Configurar la conexión desde PowerShell

El archivo `src/database/conexion.py` obtiene la dirección de conexión desde la variable de entorno `DATABASE_URL`.

Para configurar la conexión en la terminal actual:

```powershell
$env:DATABASE_URL="postgresql+psycopg://postgres:TU_CONTRASENA@localhost:5432/liquidaciones_db"
```

Se debe reemplazar `TU_CONTRASENA` por la contraseña real de PostgreSQL.

Esta variable permanece disponible en la terminal actual. Si se abre otra terminal, se debe configurar nuevamente.

Si la contraseña contiene caracteres especiales, estos deben codificarse correctamente en la URL de conexión. No se deben publicar credenciales reales en el README ni en el repositorio.

## 11. Configuración de ejemplo

El archivo `secret_config_sample.py` sirve como referencia para explicar cómo configurar la conexión sin incluir credenciales privadas.

La conexión utilizada por la aplicación se lee desde `DATABASE_URL`; por eso, configurar esa variable en PowerShell es suficiente para el código de conexión actual.

El archivo de ejemplo no reemplaza la configuración de la variable de entorno.

## 12. Crear las tablas con SQLAlchemy

Después de configurar la conexión, ejecutar desde la raíz del proyecto:

```powershell
py -3.14 -c "from src.database.conexion import crear_tablas; from src.model.modelo_liquidacion import ModeloLiquidacion; crear_tablas(); print('Tablas registradas:', list(ModeloLiquidacion.metadata.tables.keys()))"
```

Este comando importa el modelo y crea las tablas que estén registradas en la metadata de SQLAlchemy y que todavía no existan.

El modelo `ModeloLiquidacion` define la tabla `liquidaciones`, con los siguientes campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | INTEGER | Identificador del registro |
| `fecha_ingreso` | DATE | Fecha de ingreso |
| `fecha_retiro` | DATE | Fecha de retiro |
| `salario` | NUMERIC(12,2) | Salario mensual |
| `dias_trabajados` | INTEGER | Días registrados |
| `salario_integral` | BOOLEAN | Indica si el salario es integral |

## 13. Verificar que la tabla existe

Para consultar las tablas disponibles en PostgreSQL:

```powershell
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d liquidaciones_db -c "\dt"
```

Para revisar la estructura de la tabla:

```powershell
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d liquidaciones_db -c "\d public.liquidaciones"
```

Durante el desarrollo se comprobó que la tabla `public.liquidaciones` existe y contiene las columnas definidas en el modelo ORM.

## 14. Ejecutar el programa

Para iniciar la calculadora desde la raíz del proyecto:

```powershell
py -3.14 .\src\view\consola_usuario.py
```

El menú de consola presenta estas opciones:

```text
=== CALCULADORA DE LIQUIDACIÓN ===
1. Calcular liquidación
2. Guardar liquidación
3. Buscar liquidación por ID
4. Salir
```

Desde este menú se pueden ingresar los datos, guardar una liquidación y consultar un registro por su identificador.

## 15. Comprobar los registros guardados en PostgreSQL

Una parte importante del proyecto es verificar que los datos no solamente se muestren en la aplicación, sino que queden almacenados en PostgreSQL.

Para consultar todos los registros:

```powershell
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d liquidaciones_db -c "SELECT id, fecha_ingreso, fecha_retiro, salario, dias_trabajados, salario_integral FROM public.liquidaciones ORDER BY id;"
```

Durante el desarrollo se obtuvo este resultado para el registro de prueba que se guardó desde la aplicación:

```text
 id | fecha_ingreso | fecha_retiro |  salario   | dias_trabajados | salario_integral
----+---------------+--------------+------------+-----------------+------------------
  1 | 2026-01-01    | 2026-12-15   | 1750905.00 |              15 | f
```

Este resultado corresponde a los datos de esa ejecución, no a datos que deban aparecer obligatoriamente en una instalación nueva.

Para consultar un registro por su ID:

```powershell
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d liquidaciones_db -c "SELECT * FROM public.liquidaciones WHERE id = 1;"
```

Para contar cuántas liquidaciones hay almacenadas:

```powershell
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d liquidaciones_db -c "SELECT COUNT(*) AS total_liquidaciones FROM public.liquidaciones;"
```

Estas consultas permiten verificar directamente la persistencia de los datos en la base de datos.

## 16. Ejecutar las pruebas automatizadas

El proyecto utiliza Pytest para revisar las operaciones del controlador y la lógica de liquidación.

Antes de ejecutar las pruebas, comprobar que `DATABASE_URL` esté configurada.

Para ejecutar todas las pruebas:

```powershell
py -3.14 -m pytest -v
```

Para ejecutar solamente las pruebas del controlador:

```powershell
py -3.14 -m pytest tests/test_controller_liquidacion.py -v
```

Para ejecutar las pruebas de la lógica de liquidación:

```powershell
py -3.14 -m pytest tests/test_liq_def.py -v
```

En una ejecución realizada durante el desarrollo se obtuvo el siguiente resultado:

```text
20 passed
```

Esto significa que las 20 pruebas de esa ejecución finalizaron correctamente.

Entre los casos que se prueban están:

- Insertar una liquidación correctamente.
- Buscar una liquidación existente.
- Buscar una liquidación que no existe.
- Rechazar un salario inválido.
- Rechazar una fecha de retiro anterior a la fecha de ingreso.
- Rechazar días trabajados inválidos.
- Eliminar un registro existente.
- Intentar eliminar un registro inexistente.
- Comprobar la creación y eliminación de tablas.

### Importante sobre las pruebas

La prueba de eliminación de tablas y la limpieza de la fixture pueden borrar la tabla `liquidaciones`.

Por ese motivo, las pruebas deben ejecutarse en una base de datos exclusiva para pruebas, separada de la base de datos que contiene los registros que se desean conservar.

No ejecutar las pruebas destructivas contra una base de datos con información importante.

## 17. Problemas comunes

### La variable `DATABASE_URL` no está configurada

Configurar nuevamente la variable de entorno en la terminal de PowerShell antes de ejecutar el programa o las pruebas.

### No existe la tabla `liquidaciones`

Comprobar que se está conectado a `liquidaciones_db` y ejecutar el comando de creación de tablas con SQLAlchemy.

### No se ve la contraseña al escribirla

Es el comportamiento normal de la solicitud de contraseña de PostgreSQL en la terminal. Escribirla y presionar Enter.

### PostgreSQL no responde

Comprobar el estado del servicio y el puerto 5432 con los comandos indicados anteriormente.

### No aparece un registro al consultar

Verificar que la aplicación y el comando `psql` estén utilizando la misma base de datos y que la operación de guardado haya finalizado correctamente.

## 18. Conclusión

Con este proyecto se integraron Python y PostgreSQL para construir una aplicación de consola que calcula, guarda y consulta liquidaciones definitivas.

También se trabajó con el modelo ORM, las operaciones del controlador y las pruebas automatizadas para revisar los casos normales y los errores de entrada.

La consulta directa en PostgreSQL permitió comprobar que los registros guardados desde la aplicación quedan almacenados en la tabla `liquidaciones`.

El proyecto reúne la lógica de negocio, el acceso a los datos, la interfaz de usuario y las pruebas en una estructura organizada.