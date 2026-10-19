"""Inicializa las tablas de la base de datos."""

from src.controller.liquidacion_controller import crear_tablas


def main() -> None:
    """Crea las tablas registradas en los modelos."""
    crear_tablas()
    print("Tablas creadas correctamente en PostgreSQL.")


if __name__ == "__main__":
    main()
