import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QListWidget, QTextEdit, QMessageBox, QInputDialog

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()

        self.setWindowTitle("Sistema de Monitoreo de Salud")

        layout_principal = QVBoxLayout()

        # Widget que contiene todos los elementos de la interfaz
        widget_principal = QWidget()
        widget_principal.setLayout(layout_principal)
        self.setCentralWidget(widget_principal)

        # Etiqueta de Lista de Pacientes
        lbl_pacientes = QLabel("Lista de Pacientes")
        layout_principal.addWidget(lbl_pacientes)

        # Lista de Pacientes
        self.lista_pacientes = QListWidget()
        layout_principal.addWidget(self.lista_pacientes)

        # Botón Agregar Paciente
        self.boton_agregar_paciente = QPushButton("Agregar Paciente")
        layout_principal.addWidget(self.boton_agregar_paciente)

        # Botón Ver Mediciones
        self.boton_ver_mediciones = QPushButton("Ver Mediciones")
        layout_principal.addWidget(self.boton_ver_mediciones)

        # Detalles del Paciente y sus Mediciones
        lbl_detalles = QLabel("Detalles del Paciente y sus Mediciones")
        layout_principal.addWidget(lbl_detalles)

        self.texto_detalles = QTextEdit()
        layout_principal.addWidget(self.texto_detalles)

        # Botón Agregar Medición
        self.boton_agregar_medicion = QPushButton("Agregar Medición")
        layout_principal.addWidget(self.boton_agregar_medicion)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
    sys.exit(app.exec_())