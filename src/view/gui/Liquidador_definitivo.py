import sys
sys.path.append("src")
from model.logica_liquidacion_definitiva import (
    CalculadoraLiquidacionDefinitiva,
    FechasInvalidas,
    SalarioNegativo,
    DiasPendientesInvalidos,
    AuxilioTransporteInvalido,
)
from datetime import date

from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button  
from kivy.uix.gridlayout import GridLayout
from model.logica_liquidacion_definitiva import CalculadoraLiquidacionDefinitiva


class LiquidadorDefinitivoApp(App):
    def build( self):
        contenedor = GridLayout(cols=2, padding=20, spacing=20)
        contenedor.add_widget(Label(text="Calculadora de Liquidación Definitiva", font_size=20, bold=True, size_hint=(1, 0.5)))
        contenedor.add_widget(Label(text="Ingrese los datos solicitados", font_size=20, bold=True, size_hint=(1, 0.5)))
        dia_ingreso = Label(text="Ingrese el dia de Ingreso", font_size=20, size_hint=(1, 0.5))
        contenedor.add_widget(dia_ingreso)
        self.fecha_input = TextInput()
        contenedor.add_widget(self.fecha_input)
        mes_ingreso = Label(text="Ingrese el mes de Ingreso", font_size=20, size_hint=(1, 0.5))
        contenedor.add_widget(mes_ingreso)
        self.mes_input = TextInput()
        contenedor.add_widget(self.mes_input)
        ano_ingreso = Label(text="Ingrese el año de Ingreso", font_size=20,  size_hint=(1, 0.5))
        contenedor.add_widget(ano_ingreso)
        self.ano_input = TextInput()
        contenedor.add_widget(self.ano_input)
        dia_retiro = Label(text="Ingrese el dia de Retiro", font_size=20, size_hint=(1, 0.5))
        contenedor.add_widget(dia_retiro)   
        self.dia_retiro_input = TextInput()
        contenedor.add_widget(self.dia_retiro_input)
        mes_retiro = Label(text="Ingrese el mes de Retiro", font_size=20,size_hint=(1, 0.5))
        contenedor.add_widget(mes_retiro)
        self.mes_retiro_input = TextInput()
        contenedor.add_widget(self.mes_retiro_input)
        ano_retiro = Label(text="Ingrese el año de Retiro", font_size=20, size_hint=(1, 0.5))
        contenedor.add_widget(ano_retiro)
        self.ano_retiro_input = TextInput()
        contenedor.add_widget(self.ano_retiro_input)
        Sueldo= Label(text="Ingrese el monto del sueldo pactado", font_size=20, size_hint=(1, 0.5))
        contenedor.add_widget(Sueldo)
        self.Sueldo_input = TextInput()
        contenedor.add_widget(self.Sueldo_input)
        Auxilio_transporte = Label(text="Ingrese el monto del auxilio de transporte", font_size=20,  size_hint=(1, 0.5))
        contenedor.add_widget(Auxilio_transporte)
        self.auxilio_transporte_input = TextInput()
        contenedor.add_widget(self.auxilio_transporte_input)
        Dias_pendientes = Label(text="Ingrese los días pendientes de pago del último mes", font_size=20,  size_hint=(1, 0.5))
        contenedor.add_widget(Dias_pendientes)
        self.dias_pendientes_input = TextInput()
        contenedor.add_widget(self.dias_pendientes_input)
        salario_integral = Label(text="Ingrese si el empleado tiene salario integral (si/no)", font_size=20, size_hint=(1, 0.5))
        contenedor.add_widget(salario_integral)
        self.salario_integral_input = TextInput()
        contenedor.add_widget(self.salario_integral_input)
        self.resultado_label = Label(text="")
        contenedor.add_widget(self.resultado_label)

        BOTON = Button(text="Liquidar", size_hint=(1, 0.5))
        BOTON.bind(on_press=self.liquidar)
        contenedor.add_widget(BOTON)
        return contenedor


    def liquidar(self, instance):
        try:
            Fecha_ingreso = date(int(self.ano_input.text), int(self.mes_input.text), int(self.fecha_input.text))
            Fecha_retiro = date(int(self.ano_retiro_input.text), int(self.mes_retiro_input.text), int(self.dia_retiro_input.text))
            sueldo_mensual = float(self.Sueldo_input.text)
            auxilio_transporte = float(self.auxilio_transporte_input.text)
            salario_total = (sueldo_mensual + auxilio_transporte)
            dias_pendientes = int(self.dias_pendientes_input.text)
        except Exception:
            self.resultado_label.text = "Por favor, ingrese valores numéricos válidos." 
            return

        salario_integral = self.salario_integral_input.text.lower() == "si"
        liquidador = CalculadoraLiquidacionDefinitiva()

        try:
            resultado = liquidador.calcular(
                ingreso=Fecha_ingreso,
                retiro=Fecha_retiro,
                sueldo_mensual=sueldo_mensual,
                sueldo_total=salario_total,
                dias_pendientes=dias_pendientes,
                es_salario_integral=salario_integral
            )
        except (FechasInvalidas, SalarioNegativo, DiasPendientesInvalidos, AuxilioTransporteInvalido) as error:
            self.resultado_label.text = str(error)
            return
            

        self.resultado_label.text = (

    f"El monto a pagar es: {resultado['Liquidación total']}")

if __name__ == '__main__':
    LiquidadorDefinitivoApp().run()

