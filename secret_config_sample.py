
"""
Configuración de ejemplo para conectar el proyecto con PostgreSQL.

Para ejecutar el programa, hay que configurar la variable DATABASE_URL
en PowerShell con los datos de la base de datos.

Cambia el usuario y la contraseña de ejemplo por los tuyos.
No compartas tus datos de conexión reales.
"""

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://USUARIO:CONTRASENA@localhost:5432/liquidaciones_db",
)