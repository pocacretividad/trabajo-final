from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QComboBox, QSizePolicy, QGroupBox, QDialog  # Agregar importación de QDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from datetime import datetime
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from modelo import Paciente

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro y análisis de pacientes con hígado graso")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout_principal = QVBoxLayout()
        self.central_widget.setLayout(self.layout_principal)

        self.label_titulo = QLabel("Registro y análisis de pacientes con hígado graso")
        self.layout_principal.addWidget(self.label_titulo)

        self.boton_agregar_paciente = QPushButton("Agregar Paciente")
        self.boton_agregar_paciente.clicked.connect(self.mostrar_formulario_paciente)
        self.layout_principal.addWidget(self.boton_agregar_paciente)

        self.layout_pacientes = QVBoxLayout()
        self.layout_principal.addLayout(self.layout_pacientes)

    def mostrar_formulario_paciente(self):
        self.formulario_paciente = FormularioPaciente()
        self.formulario_paciente.paciente_agregado.connect(self.agregar_paciente)
        self.formulario_paciente.show()

    def agregar_paciente(self, paciente):
        paciente_widget = PacienteWidget(paciente)
        self.layout_pacientes.addWidget(paciente_widget)

class FormularioPaciente(QWidget):
    paciente_agregado = QtCore.pyqtSignal(Paciente)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label_nombre = QLabel("Nombre:")
        self.input_nombre = QLineEdit()
        self.layout.addWidget(self.label_nombre)
        self.layout.addWidget(self.input_nombre)

        self.label_apellido = QLabel("Apellido:")
        self.input_apellido = QLineEdit()
        self.layout.addWidget(self.label_apellido)
        self.layout.addWidget(self.input_apellido)

        self.label_edad = QLabel("Edad:")
        self.input_edad = QLineEdit()
        self.layout.addWidget(self.label_edad)
        self.layout.addWidget(self.input_edad)

        self.label_id = QLabel("ID:")
        self.input_id = QLineEdit()
        self.layout.addWidget(self.label_id)
        self.layout.addWidget(self.input_id)

        self.boton_seleccionar_imagen = QPushButton("Seleccionar Imagen")
        self.boton_seleccionar_imagen.clicked.connect(self.seleccionar_imagen)
        self.layout.addWidget(self.boton_seleccionar_imagen)

        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.guardar_paciente)
        self.layout.addWidget(self.boton_guardar)

    def seleccionar_imagen(self):
        ruta_imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg)")
        if ruta_imagen:
            self.ruta_imagen = ruta_imagen

    def guardar_paciente(self):
        nombre = self.input_nombre.text()
        apellido = self.input_apellido.text()
        edad = int(self.input_edad.text())
        id_paciente = int(self.input_id.text())

        if nombre and apellido and edad and id_paciente and hasattr(self, 'ruta_imagen'):
            fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            paciente = Paciente(id_paciente, nombre, apellido, edad, fecha_registro)
            paciente.agregar_imagen(self.ruta_imagen, fecha_registro)
            self.paciente_agregado.emit(paciente)
            self.close()

class PacienteWidget(QWidget):
    def __init__(self, paciente):
        super().__init__()
        self.paciente = paciente

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label_nombre = QLabel(f"Nombre: {self.paciente.nombre}")
        self.layout.addWidget(self.label_nombre)

        self.label_apellido = QLabel(f"Apellido: {self.paciente.apellido}")
        self.layout.addWidget(self.label_apellido)

        self.label_edad = QLabel(f"Edad: {self.paciente.edad}")
        self.layout.addWidget(self.label_edad)

        self.label_id = QLabel(f"ID: {self.paciente.id_paciente}")
        self.layout.addWidget(self.label_id)

        self.label_imagen = QLabel("Imagen:")
        self.imagen = QLabel()
        self.imagen.setPixmap(QPixmap(self.paciente.imagenes[0][0]))
        self.layout.addWidget(self.label_imagen)
        self.layout.addWidget(self.imagen)

        self.boton_agregar_imagen = QPushButton("Agregar Imagen")
        self.boton_agregar_imagen.clicked.connect(self.agregar_imagen)
        self.layout.addWidget(self.boton_agregar_imagen)

        self.boton_ver_analisis = QPushButton("Ver Análisis")
        self.boton_ver_analisis.clicked.connect(self.ver_analisis)
        self.layout.addWidget(self.boton_ver_analisis)

    def agregar_imagen(self):
        ruta_imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg)")
        if ruta_imagen:
            self.paciente.agregar_imagen(ruta_imagen, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.imagen.setPixmap(QPixmap(self.paciente.imagenes[-1][0]))

    def ver_analisis(self):
        analisis_dialog = AnalisisDialog(self.paciente)
        analisis_dialog.exec_()

class AnalisisDialog(QDialog):
    def __init__(self, paciente):
        super().__init__()

        self.setWindowTitle("Análisis del Paciente")
        self.setGeometry(200, 200, 600, 400)

        self.paciente = paciente

        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)

        self.label_titulo = QLabel(f"Análisis del Paciente {self.paciente.id_paciente}")
        self.layout_principal.addWidget(self.label_titulo)

        self.layout_grafica = QVBoxLayout()
        self.layout_principal.addLayout(self.layout_grafica)

        self.mostrar_grafica()

    def mostrar_grafica(self):
        fig, ax = plt.subplots()
        ax.bar(["Hígado"], [self.paciente.calcular_grasa_higado()], color='blue')
        ax.set_ylabel('Porcentaje de Grasa en el Hígado')
        ax.set_title('Análisis de Grasa en el Hígado')
        ax.set_ylim(0, 100)
        canvas = FigureCanvas(fig)
        self.layout_grafica.addWidget(canvas)
