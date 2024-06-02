from PyQt5.QtWidgets import QApplication
import sys
from modelo import BaseDatos, Paciente
from vista import VentanaPrincipal

class Controlador:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.vista = VentanaPrincipal()
        self.base_datos = BaseDatos('pacientes.db')
        self.cargar_pacientes()
        self.conectar_eventos()
    
    def conectar_eventos(self):
        self.vista.mostrar_formulario_paciente()
        self.vista.formulario_paciente.paciente_agregado.connect(self.agregar_paciente)
        self.vista.closeEvent = self.guardar_datos_salir
    
    def cargar_pacientes(self):
        for id_paciente in self.base_datos.obtener_lista_pacientes():
            paciente = self.base_datos.obtener_paciente(id_paciente)
            if paciente:
                self.vista.agregar_paciente(paciente)

    def agregar_paciente(self, paciente):
        self.base_datos.agregar_paciente(paciente)
        self.vista.agregar_paciente(paciente)

    def guardar_datos_salir(self, event):
        self.base_datos.cerrar_conexion()
        self.app.quit()

    def ejecutar(self):
        self.vista.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controlador = Controlador()
    controlador.ejecutar()
