from PyQt5.QtWidgets import QApplication
import sys
from modelo import BaseDatos, Paciente
from vista import VentanaPrincipal

class Controlador:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.base_datos = BaseDatos('pacientes.db')
        self.vista = VentanaPrincipal(self.base_datos)
        self.conectar_eventos()
        self.vista.cargar_pacientes()

    def conectar_eventos(self):
        self.vista.boton_agregar_paciente.clicked.connect(self.mostrar_formulario_paciente)
        self.vista.boton_buscar_paciente.clicked.connect(self.buscar_paciente)
        self.vista.boton_ver_todos_pacientes.clicked.connect(self.ver_todos_pacientes)
        self.vista.closeEvent = self.guardar_datos_salir

    def mostrar_formulario_paciente(self):
        self.vista.mostrar_formulario_paciente()

    def buscar_paciente(self):
        self.vista.buscar_paciente()

    def ver_todos_pacientes(self):
        self.vista.ver_todos_pacientes()

    def guardar_datos_salir(self, event):
        self.base_datos.cerrar_conexion()
        self.app.quit()

    def ejecutar(self):
        self.vista.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controlador = Controlador()
    controlador.ejecutar()
    
    
    
    