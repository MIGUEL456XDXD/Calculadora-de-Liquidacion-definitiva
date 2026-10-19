"""Interfaz gráfica en Kivy para la calculadora y gestión de liquidaciones."""

import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from src.controller import liquidacion_controller as controlador
from src.model import logica_liquidacion_definitiva as logica


class LiquidacionKivyLayout(BoxLayout):
    """Contenedor principal de la interfaz gráfica."""

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=15, spacing=10, **kwargs)

        titulo = Label(
            text="CALCULADORA Y GESTOR DE LIQUIDACIONES",
            size_hint_y=None,
            height=40,
            bold=True,
        )
        self.add_widget(titulo)

        # --- Formulario de entrada de datos ---
        formulario = GridLayout(cols=2, spacing=8, size_hint_y=None, height=240)

        formulario.add_widget(Label(text="Fecha ingreso (AAAA-MM-DD):"))
        self.input_ingreso = TextInput(
            hint_text="2026-01-01", multiline=False
        )
        formulario.add_widget(self.input_ingreso)

        formulario.add_widget(Label(text="Fecha retiro (AAAA-MM-DD):"))
        self.input_retiro = TextInput(
            hint_text="2026-12-15", multiline=False
        )
        formulario.add_widget(self.input_retiro)

        formulario.add_widget(Label(text="Salario mensual ($):"))
        self.input_salario = TextInput(
            hint_text="1750905", input_filter="float", multiline=False
        )
        formulario.add_widget(self.input_salario)

        formulario.add_widget(Label(text="Auxilio transporte (0 si no aplica):"))
        self.input_auxilio = TextInput(
            text="0", input_filter="float", multiline=False
        )
        formulario.add_widget(self.input_auxilio)

        formulario.add_widget(Label(text="Días trabajados / pendientes (0-30):"))
        self.input_dias = TextInput(
            hint_text="15", input_filter="int", multiline=False
        )
        formulario.add_widget(self.input_dias)

        formulario.add_widget(Label(text="¿Tiene salario integral?:"))
        self.check_integral = CheckBox(active=False)
        formulario.add_widget(self.check_integral)

        self.add_widget(formulario)

        # --- Botones de acción principales (Insertar, Calcular, Tablas) ---
        panel_botones = GridLayout(cols=2, spacing=8, size_hint_y=None, height=90)

        btn_insertar = Button(text="Insertar en BD (INSERT)")
        btn_insertar.bind(on_press=self.accion_insertar)
        panel_botones.add_widget(btn_insertar)

        btn_calcular = Button(text="Calcular Liquidación")
        btn_calcular.bind(on_press=self.accion_calcular)
        panel_botones.add_widget(btn_calcular)

        btn_crear_tablas = Button(text="Crear Tablas en BD")
        btn_crear_tablas.bind(on_press=self.accion_crear_tablas)
        panel_botones.add_widget(btn_crear_tablas)

        btn_borrar_tablas = Button(text="Borrar Tablas de BD")
        btn_borrar_tablas.bind(on_press=self.accion_borrar_tablas)
        panel_botones.add_widget(btn_borrar_tablas)

        self.add_widget(panel_botones)

        # --- Sección de Búsqueda por ID (SELECT) ---
        panel_busqueda = BoxLayout(
            orientation="horizontal", spacing=8, size_hint_y=None, height=45
        )
        panel_busqueda.add_widget(Label(text="Buscar por ID:", size_hint_x=0.3))
        self.input_id_buscar = TextInput(
            hint_text="Ej: 1",
            input_filter="int",
            multiline=False,
            size_hint_x=0.3,
        )
        panel_busqueda.add_widget(self.input_id_buscar)

        btn_buscar = Button(
            text="Consultar en BD (SELECT)", size_hint_x=0.4
        )
        btn_buscar.bind(on_press=self.accion_buscar)
        panel_busqueda.add_widget(btn_buscar)

        self.add_widget(panel_busqueda)

        # --- Área de Resultados y Mensajes ---
        self.salida_texto = TextInput(
            text="Listo. Usa los botones para crear tablas, insertar o buscar.",
            readonly=True,
            size_hint_y=1,
        )
        self.add_widget(self.salida_texto)

    def _leer_fechas(self) -> tuple[date, date]:
        """Convierte los textos de fecha en objetos date."""
        ingreso = date.fromisoformat(self.input_ingreso.text.strip())
        retiro = date.fromisoformat(self.input_retiro.text.strip())
        return ingreso, retiro

    def accion_crear_tablas(self, _instance) -> None:
        """Ejecuta la creación de tablas desde el controlador."""
        try:
            controlador.crear_tablas()
            self.salida_texto.text = (
                "ÉXITO: Las tablas fueron creadas correctamente en PostgreSQL."
            )
        except Exception as error:
            self.salida_texto.text = f"Error al crear las tablas:\n{error}"

    def accion_borrar_tablas(self, _instance) -> None:
        """Ejecuta el borrado de tablas desde el controlador."""
        try:
            controlador.borrar_tablas()
            self.salida_texto.text = (
                "ÉXITO: Las tablas fueron eliminadas de la base de datos."
            )
        except Exception as error:
            self.salida_texto.text = f"Error al borrar las tablas:\n{error}"

    def accion_insertar(self, _instance) -> None:
        """Guarda una liquidación en la base de datos usando el controlador."""
        try:
            ingreso, retiro = self._leer_fechas()
            salario = Decimal(self.input_salario.text.strip())
            dias = int(self.input_dias.text.strip())
            es_integral = bool(self.check_integral.active)

            nuevo_id = controlador.insertar_liquidacion(
                fecha_ingreso=ingreso,
                fecha_retiro=retiro,
                salario=salario,
                dias_trabajados=dias,
                salario_integral=es_integral,
            )
            self.salida_texto.text = (
                f"ÉXITO: Liquidación insertada en la base de datos.\n"
                f"ID asignado: {nuevo_id}"
            )
        except (ValueError, InvalidOperation) as error:
            self.salida_texto.text = f"Datos inválidos:\n{error}"
        except Exception as error:
            self.salida_texto.text = (
                f"Error en la base de datos al insertar:\n{error}"
            )

    def accion_buscar(self, _instance) -> None:
        """Consulta una liquidación por su ID usando el controlador."""
        try:
            texto_id = self.input_id_buscar.text.strip()
            if not texto_id:
                self.salida_texto.text = "Por favor ingresa un ID para buscar."
                return

            identificador = int(texto_id)
            liquidacion = controlador.buscar_liquidacion(identificador)

            if liquidacion is None:
                self.salida_texto.text = (
                    f"No se encontró ninguna liquidación con el ID {identificador}."
                )
                return

            integral_txt = "Sí" if liquidacion.salario_integral else "No"
            self.salida_texto.text = (
                f"=== REGISTRO ENCONTRADO ===\n"
                f"ID: {liquidacion.id}\n"
                f"Fecha de ingreso: {liquidacion.fecha_ingreso}\n"
                f"Fecha de retiro: {liquidacion.fecha_retiro}\n"
                f"Salario mensual: ${liquidacion.salario}\n"
                f"Días trabajados: {liquidacion.dias_trabajados}\n"
                f"Salario integral: {integral_txt}"
            )
        except ValueError as error:
            self.salida_texto.text = f"Error de validación:\n{error}"
        except Exception as error:
            self.salida_texto.text = f"Error al consultar la BD:\n{error}"

    def accion_calcular(self, _instance) -> None:
        """Calcula los valores de la liquidación definitiva en pantalla."""
        try:
            ingreso, retiro = self._leer_fechas()
            sueldo = float(self.input_salario.text.strip())
            auxilio = float(self.input_auxilio.text.strip() or 0)
            dias = int(self.input_dias.text.strip())
            es_integral = bool(self.check_integral.active)

            datos = logica.DatosLiquidacion(
                ingreso=ingreso,
                retiro=retiro,
                sueldo_mensual=sueldo,
                salario_total=sueldo + auxilio,
                dias_pendientes=dias,
                es_salario_integral=es_integral,
            )
            resultado = logica.calcular_liquidacion_definitiva(datos)

            lineas = ["=== RESULTADO DEL CÁLCULO ==="]
            for clave, valor in resultado.items():
                lineas.append(f"{clave}: {valor}")
            self.salida_texto.text = "\n".join(lineas)

        except Exception as error:
            self.salida_texto.text = f"Error en el cálculo:\n{error}"


class CalculadoraLiquidacionApp(App):
    """Aplicación principal de Kivy."""

    def build(self):
        self.title = "Calculadora de Liquidación Definitiva"
        return LiquidacionKivyLayout()


if __name__ == "__main__":
    CalculadoraLiquidacionApp().run()
