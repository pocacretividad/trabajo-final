from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QScrollArea, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import cv2
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
        self.layout_principal.addWidget(self.boton_agregar_paciente)

        self.boton_buscar_paciente = QPushButton("Buscar Paciente")
        self.layout_principal.addWidget(self.boton_buscar_paciente)

        self.boton_ver_todos_pacientes = QPushButton("Ver Todos los Pacientes")
        self.layout_principal.addWidget(self.boton_ver_todos_pacientes)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout()
        self.scroll_area_widget.setLayout(self.scroll_area_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.layout_principal.addWidget(self.scroll_area)

    def mostrar_formulario_paciente(self):
        self.formulario_paciente = FormularioPaciente(self.base_datos)
        self.formulario_paciente.paciente_agregado.connect(self.agregar_paciente)
        self.formulario_paciente.show()

    def agregar_paciente(self, paciente):
        paciente_widget = PacienteWidget(paciente, self.base_datos)
        self.scroll_area_layout.addWidget(paciente_widget)

    def buscar_paciente(self):
        self.formulario_busqueda = FormularioBusqueda(self.base_datos)
        self.formulario_busqueda.paciente_buscado.connect(self.mostrar_paciente_buscado)
        self.formulario_busqueda.show()

    def mostrar_paciente_buscado(self, id_paciente):
        for i in reversed(range(self.scroll_area_layout.count())):
            widget = self.scroll_area_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        paciente = self.base_datos.obtener_paciente(id_paciente)
        if paciente:
            paciente_widget = PacienteWidget(paciente, self.base_datos)
            self.scroll_area_layout.addWidget(paciente_widget)
        else:
            self.label_error = QLabel("Paciente no encontrado")
            self.layout_principal.addWidget(self.label_error)

    def ver_todos_pacientes(self):
        for i in reversed(range(self.scroll_area_layout.count())):
            widget = self.scroll_area_layout.itemAt(i).widget()
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
            self.imagenes.append(ruta_imagen)

    def guardar_paciente(self):
        nombre = self.input_nombre.text()
        apellido = self.input_apellido.text()
        edad = int(self.input_edad.text())
        id_paciente = int(self.input_id.text())
        fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        paciente = Paciente(id_paciente, nombre, apellido, edad, fecha_registro)

        for imagen in self.imagenes:
            fecha_toma = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            paciente.agregar_imagen(imagen, fecha_toma)

        self.base_datos.agregar_paciente(paciente)
        for imagen in paciente.imagenes:
            self.base_datos.agregar_imagen_paciente(paciente.id_paciente, imagen[0], imagen[1])

        self.paciente_agregado.emit(paciente)
        self.close()

class FormularioBusqueda(QWidget):
    paciente_buscado = QtCore.pyqtSignal(int)

    def __init__(self, base_datos):
        super().__init__()
        self.base_datos = base_datos

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label_id = QLabel("ID del Paciente:")
        self.input_id = QLineEdit()
        self.layout.addWidget(self.label_id)
        self.layout.addWidget(self.input_id)

        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar_paciente)
        self.layout.addWidget(self.boton_buscar)

    def buscar_paciente(self):
        id_paciente = int(self.input_id.text())
        self.paciente_buscado.emit(id_paciente)
        self.close()

class PacienteWidget(QWidget):
    def __init__(self, paciente, base_datos):
        super().__init__()
        self.paciente = paciente
        self.base_datos = base_datos

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label_nombre = QLabel(f"Nombre: {paciente.nombre} {paciente.apellido}")
        self.layout.addWidget(self.label_nombre)

        self.label_edad = QLabel(f"Edad: {paciente.edad}")
        self.layout.addWidget(self.label_edad)
        
        self.label_id_paciente=QLabel( f"ID: {paciente.id_paciente} ")
        self.layout.addWidget(self.label_id_paciente)

        self.label_fecha_registro = QLabel(f"Fecha de Registro: {paciente.fecha_registro}")
        self.layout.addWidget(self.label_fecha_registro)

        for imagen, fecha_toma in paciente.imagenes:
            self.mostrar_imagen(imagen, fecha_toma)

        self.boton_agregar_imagen = QPushButton("Agregar Imagen")
        self.boton_agregar_imagen.clicked.connect(self.agregar_imagen)
        self.layout.addWidget(self.boton_agregar_imagen)

        self.boton_ver_analisis = QPushButton("Ver Análisis")
        self.boton_ver_analisis.clicked.connect(self.ver_analisis)
        self.layout.addWidget(self.boton_ver_analisis)

    def mostrar_imagen(self, ruta_imagen, fecha_toma):
        label_fecha_toma = QLabel(f"Fecha de Toma: {fecha_toma}")
        self.layout.addWidget(label_fecha_toma)

        pixmap = QPixmap(ruta_imagen)
        label_imagen = QLabel()
        label_imagen.setPixmap(pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio))
        self.layout.addWidget(label_imagen)

        porcentaje_grasa = self.calcular_porcentaje_grasa(ruta_imagen)
        label_porcentaje_grasa = QLabel(f"Porcentaje de Grasa: {porcentaje_grasa:.2f}%")
        self.layout.addWidget(label_porcentaje_grasa)

    def agregar_imagen(self):
        ruta_imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg)")
        if ruta_imagen:
            fecha_toma = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.base_datos.agregar_imagen_paciente(self.paciente.id_paciente, ruta_imagen, fecha_toma)
            self.paciente.agregar_imagen(ruta_imagen, fecha_toma)
            self.mostrar_imagen(ruta_imagen, fecha_toma)

    def ver_analisis(self):
        fechas = [imagen[1] for imagen in self.paciente.imagenes]
        grasas = [self.calcular_porcentaje_grasa(imagen[0]) for imagen in self.paciente.imagenes]

        ventana_analisis = VentanaAnalisis(fechas, grasas)
        ventana_analisis.exec_()
        

    def calcular_porcentaje_grasa(self, ruta_imagen):
        imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
        umbral, imagen_binaria = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY)
        total_pixeles = imagen.size
        pixeles_blancos = cv2.countNonZero(imagen_binaria)
        pixeles_negros = total_pixeles - pixeles_blancos
        porcentaje_grasa = (pixeles_blancos / total_pixeles) * 100
        return porcentaje_grasa

class VentanaAnalisis(QDialog):
    def __init__(self, fechas, grasas):
        super().__init__()
        self.setWindowTitle("Análisis de Grasa en el Hígado")
        self.setGeometry(100, 100, 800, 600)

        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)

        # Crear el gráfico de barras
        self.fig_barras, self.ax_barras = plt.subplots(figsize=(8, 6))
        self.ax_barras.bar(fechas, grasas, color='blue')
        self.ax_barras.set_ylabel('Porcentaje de Grasa en el Hígado')
        self.ax_barras.set_title('Análisis de Grasa en el Hígado - Gráfico de Barras')
        self.ax_barras.set_ylim(0, 100)
        self.canvas_barras = FigureCanvas(self.fig_barras)
        self.layout_principal.addWidget(self.canvas_barras)

        # Crear el gráfico de líneas
        self.fig_lineas, self.ax_lineas = plt.subplots(figsize=(8, 6))
        self.ax_lineas.plot(fechas, grasas, marker='o', linestyle='-', color='green')
        self.ax_lineas.set_ylabel('Porcentaje de Grasa en el Hígado')
        self.ax_lineas.set_title('Análisis de Grasa en el Hígado - Gráfico de Líneas')
        self.ax_lineas.set_ylim(0, 100)
        self.canvas_lineas = FigureCanvas(self.fig_lineas)
        self.layout_principal.addWidget(self.canvas_lineas)

