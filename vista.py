from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QInputDialog, QGridLayout, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from modelo import Paciente

class VentanaPrincipal(QMainWindow):
    def __init__(self, base_datos):
        super().__init__()
        self.setWindowTitle("Registro y análisis de pacientes con hígado graso")
        self.setGeometry(100, 100, 800, 600)
        self.base_datos = base_datos

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout_principal = QVBoxLayout()
        self.central_widget.setLayout(self.layout_principal)

        self.label_titulo = QLabel("Registro y análisis de pacientes con hígado graso")
        self.layout_principal.addWidget(self.label_titulo)

        self.boton_agregar_paciente = QPushButton("Agregar Paciente")
        self.boton_agregar_paciente.clicked.connect(self.mostrar_formulario_paciente)
        self.layout_principal.addWidget(self.boton_agregar_paciente)

        self.boton_buscar_paciente = QPushButton("Buscar Paciente")
        self.boton_buscar_paciente.clicked.connect(self.buscar_paciente)
        self.layout_principal.addWidget(self.boton_buscar_paciente)

        self.boton_ver_todos_pacientes = QPushButton("Ver Todos los Pacientes")
        self.boton_ver_todos_pacientes.clicked.connect(self.ver_todos_pacientes)
        self.layout_principal.addWidget(self.boton_ver_todos_pacientes)

        self.layout_pacientes = QVBoxLayout()
        self.layout_principal.addLayout(self.layout_pacientes)

    def mostrar_formulario_paciente(self):
        self.formulario_paciente = FormularioPaciente(self.base_datos)
        self.formulario_paciente.paciente_agregado.connect(self.agregar_paciente)
        self.formulario_paciente.show()

    def agregar_paciente(self, paciente):
        paciente_widget = PacienteWidget(paciente, self.base_datos)
        self.layout_pacientes.addWidget(paciente_widget)

    def buscar_paciente(self):
        self.formulario_busqueda = FormularioBusqueda(self.base_datos)
        self.formulario_busqueda.paciente_buscado.connect(self.mostrar_paciente_buscado)
        self.formulario_busqueda.show()

    def mostrar_paciente_buscado(self, id_paciente):
        for i in reversed(range(self.layout_pacientes.count())):
            widget = self.layout_pacientes.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        paciente = self.base_datos.obtener_paciente(id_paciente)
        if paciente:
            paciente_widget = PacienteWidget(paciente, self.base_datos)
            self.layout_pacientes.addWidget(paciente_widget)
        else:
            self.label_error = QLabel("Paciente no encontrado")
            self.layout_principal.addWidget(self.label_error)

    def ver_todos_pacientes(self):
        for i in reversed(range(self.layout_pacientes.count())):
            widget = self.layout_pacientes.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.cargar_pacientes()

    def cargar_pacientes(self):
        for id_paciente in self.base_datos.obtener_lista_pacientes():
            paciente = self.base_datos.obtener_paciente(id_paciente)
            if paciente:
                self.agregar_paciente(paciente)

class FormularioPaciente(QWidget):
    paciente_agregado = QtCore.pyqtSignal(Paciente)

    def __init__(self, base_datos):
        super().__init__()
        self.base_datos = base_datos

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

        self.imagenes = []

    def seleccionar_imagen(self):
        ruta_imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg)")
        if ruta_imagen:
            fecha_toma, ok = QInputDialog.getText(self, "Fecha de Toma", "Ingrese la fecha de toma (YYYY-MM-DD):")
            if ok:
                self.imagenes.append((ruta_imagen, fecha_toma))

    def guardar_paciente(self):
        nombre = self.input_nombre.text()
        apellido = self.input_apellido.text()
        edad = int(self.input_edad.text())
        id_paciente = int(self.input_id.text())

        if nombre and apellido and edad and id_paciente and self.imagenes:
            fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            paciente = Paciente(id_paciente, nombre, apellido, edad, fecha_registro)
            for ruta_imagen, fecha_toma in self.imagenes:
                paciente.agregar_imagen(ruta_imagen, fecha_toma)
                self.base_datos.agregar_imagen_paciente(id_paciente, ruta_imagen, fecha_toma)
            self.paciente_agregado.emit(paciente)
            self.close()

class PacienteWidget(QWidget):
    def __init__(self, paciente, base_datos):
        super().__init__()
        self.paciente = paciente
        self.base_datos = base_datos

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

        self.layout_imagenes = QGridLayout()
        self.layout.addLayout(self.layout_imagenes)

        self.mostrar_imagenes()

        self.boton_agregar_imagen = QPushButton("Agregar Imagen")
        self.boton_agregar_imagen.clicked.connect(self.agregar_imagen)
        self.layout.addWidget(self.boton_agregar_imagen)

        self.boton_ver_analisis = QPushButton("Ver Análisis")
        self.boton_ver_analisis.clicked.connect(self.ver_analisis)
        self.layout.addWidget(self.boton_ver_analisis)

    def mostrar_imagenes(self):
        for i in range(self.layout_imagenes.count()):
            self.layout_imagenes.itemAt(i).widget().deleteLater()
        
        for i, (ruta_imagen, fecha_toma) in enumerate(self.paciente.imagenes):
            label_imagen = QLabel()
            label_imagen.setPixmap(QPixmap(ruta_imagen).scaled(100, 100, QtCore.Qt.KeepAspectRatio))
            self.layout_imagenes.addWidget(label_imagen, i // 3, i % 3)
            label_fecha = QLabel(fecha_toma)
            self.layout_imagenes.addWidget(label_fecha, i // 3, (i % 3) + 1)

    def agregar_imagen(self):
        ruta_imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg)")
        if ruta_imagen:
            fecha_toma, ok = QInputDialog.getText(self, "Fecha de Toma", "Ingrese la fecha de toma (YYYY-MM-DD):")
            if ok:
                self.paciente.agregar_imagen(ruta_imagen, fecha_toma)
                self.base_datos.agregar_imagen_paciente(self.paciente.id_paciente, ruta_imagen, fecha_toma)
                self.mostrar_imagenes()

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
        fechas = [imagen[1] for imagen in self.paciente.imagenes]
        grasas = [self.paciente.calcular_porcentaje_grasa(imagen[0]) for imagen in self.paciente.imagenes]

        fig, ax = plt.subplots(2, 1, figsize=(8, 6))

        ax[0].bar(fechas, grasas, color='blue')
        ax[0].set_ylabel('Porcentaje de Grasa en el Hígado')
        ax[0].set_title('Análisis de Grasa en el Hígado')
        ax[0].set_ylim(0, 100)

        ax[1].plot(fechas, grasas, marker='o')
        ax[1].set_ylabel('Porcentaje de Grasa en el Hígado')
        ax[1].set_title('Evolución de la Grasa en el Hígado')
        ax[1].set_ylim(0, 100)

        plt.tight_layout()

        canvas = FigureCanvas(fig)
        self.layout_grafica.addWidget(canvas)

class FormularioBusqueda(QWidget):
    paciente_buscado = QtCore.pyqtSignal(int)

    def __init__(self, base_datos):
        super().__init__()
        self.base_datos = base_datos

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label_id = QLabel("Ingrese el ID del Paciente:")
        self.input_id = QLineEdit()
        self.layout.addWidget(self.label_id)
        self.layout.addWidget(self.input_id)

        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar_paciente)
        self.layout.addWidget(self.boton_buscar)

    def buscar_paciente(self):
        id_paciente = int(self.input_id.text())
        self.paciente_buscado.emit(id_paciente)



