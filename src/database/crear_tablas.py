"""Inicializa las tablas de la base de datos."""

from src.database.conexion import crear_tablas
from src.model.modelo_liquidacion import ModeloLiquidacion


def main():
    """Crea las tablas registradas en los modelos."""
    crear_tablas()
    print("Tablas creadas correctamente en PostgreSQL.")


if __name__ == "__main__":
    main()