import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QListWidget, QTextEdit, QMessageBox, QInputDialog, QListWidgetItem
#from modelo.base_de_datos import BaseDeDatos
from modelo import BaseDeDatos

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()

        self.setWindowTitle("Sistema de Monitoreo de Salud")
        self.setGeometry(100, 100, 600, 400)

        layout_principal = QVBoxLayout()
        widget_principal = QWidget()
        widget_principal.setLayout(layout_principal)
        self.setCentralWidget(widget_principal)

        lbl_pacientes = QLabel("Lista de Pacientes")
        layout_principal.addWidget(lbl_pacientes)

        self.lista_pacientes = QListWidget()
        layout_principal.addWidget(self.lista_pacientes)

        self.boton_agregar_paciente = QPushButton("Agregar Paciente")
        layout_principal.addWidget(self.boton_agregar_paciente)

        self.boton_ver_mediciones = QPushButton("Ver Mediciones")
        layout_principal.addWidget(self.boton_ver_mediciones)

        lbl_detalles = QLabel("Detalles del Paciente y sus Mediciones")
        layout_principal.addWidget(lbl_detalles)

        self.texto_detalles = QTextEdit()
        layout_principal.addWidget(self.texto_detalles)

        self.boton_agregar_medicion = QPushButton("Agregar Medición")
        layout_principal.addWidget(self.boton_agregar_medicion)

        self.base_de_datos = BaseDeDatos()
        self.cargar_pacientes()
        self.boton_agregar_paciente.clicked.connect(self.agregar_paciente)
        self.boton_ver_mediciones.clicked.connect(self.ver_mediciones)
        self.boton_agregar_medicion.clicked.connect(self.agregar_medicion)

    def cargar_pacientes(self):
        pacientes = self.base_de_datos.obtener_pacientes()
        self.lista_pacientes.clear()
        for paciente in pacientes:
            item = QListWidgetItem(f"{paciente[1]} - {paciente[2]} años - {paciente[3]}")
            item.setData(1, paciente[0])
            self.lista_pacientes.addItem(item)

    def agregar_paciente(self):
        nombre, ok1 = QInputDialog.getText(self, 'Agregar Paciente', 'Nombre:')
        if not ok1 or not nombre:
            return
        edad, ok2 = QInputDialog.getInt(self, 'Agregar Paciente', 'Edad:')
        if not ok2:
            return
        genero, ok3 = QInputDialog.getText(self, 'Agregar Paciente', 'Género:')
        if not ok3 or not genero:
            return
        diagnostico, ok4 = QInputDialog.getText(self, 'Agregar Paciente', 'Diagnóstico:')
        if not ok4 or not diagnostico:
            return
        
        self.base_de_datos.agregar_paciente(nombre, edad, genero, diagnostico)
        self.cargar_pacientes()

    def ver_mediciones(self):
        item_actual = self.lista_pacientes.currentItem()
        if not item_actual:
            QMessageBox.warning(self, 'Advertencia', 'Seleccione un paciente.')
            return
        paciente_id = item_actual.data(1)
        mediciones = self.base_de_datos.obtener_mediciones(paciente_id)
        detalles = f"Mediciones de {item_actual.text()}:\n"
        for medicion in mediciones:
            detalles += f"Fecha: {medicion[0]}, Tipo: {medicion[1]}, Valor: {medicion[2]}\n"
        self.texto_detalles.setText(detalles)

    def agregar_medicion(self):
        item_actual = self.lista_pacientes.currentItem()
        if not item_actual:
            QMessageBox.warning(self, 'Advertencia', 'Seleccione un paciente.')
            return
        paciente_id = item_actual.data(1)
        tipo_medicion, ok1 = QInputDialog.getText(self, 'Agregar Medición', 'Tipo de Medición:')
        if not ok1 or not tipo_medicion:
            return
        valor, ok2 = QInputDialog.getDouble(self, 'Agregar Medición', 'Valor:')
        if not ok2:
            return

        self.base_de_datos.agregar_medicion(paciente_id, tipo_medicion, valor)
        self.ver_mediciones()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
    sys.exit(app.exec_())