from sqlalchemy import text
from src.database.conexion import engine

try:
    with engine.connect() as conexion:
        print(
            "Base de datos:",
            conexion.execute(
                text("SELECT current_database()")
            ).scalar(),
        )

        tablas = conexion.execute(
            text("""
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_name = 'liquidaciones'
            """)
        ).fetchall()

        print("Tabla liquidaciones:", tablas)

except Exception as error:
    print("Error:", error)