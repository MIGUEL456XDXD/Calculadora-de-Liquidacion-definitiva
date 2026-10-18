
"""
Configuración de ejemplo para conectar el proyecto
de liquidación definitiva con PostgreSQL.

Antes de ejecutar el programa, hay que configurar
la variable DATABASE_URL desde PowerShell.

Los datos que aparecen abajo son de ejemplo.
Cambia el usuario y la contraseña según tu configuración.
No compartas tus datos reales de conexión.
"""

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://USUARIO:CONTRASENA@localhost:5432/liquidaciones_db",
)