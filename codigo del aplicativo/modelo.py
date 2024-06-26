import sqlite3
import cv2
import numpy as np
from datetime import datetime

class Paciente:
    def __init__(self, id_paciente, nombre, apellido, edad, fecha_registro):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.fecha_registro = fecha_registro
        self.imagenes = []

    def agregar_imagen(self, ruta_imagen, fecha_toma):
        self.imagenes.append((ruta_imagen, fecha_toma))

class BaseDatos:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()
        self.crear_tabla_pacientes()
        self.crear_tabla_imagenes()

    def crear_tabla_pacientes(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pacientes (
                                id INTEGER PRIMARY KEY,
                                nombre TEXT,
                                apellido TEXT,
                                edad INTEGER,
                                fecha_registro TEXT
                            )''')
        self.conexion.commit()

    def crear_tabla_imagenes(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS imagenes (
                                id_paciente INTEGER,
                                ruta TEXT,
                                fecha_toma TEXT,
                                FOREIGN KEY (id_paciente) REFERENCES pacientes(id)
                            )''')
        self.conexion.commit()

    def agregar_paciente(self, paciente):
        self.cursor.execute('''INSERT INTO pacientes 
                                (id, nombre, apellido, edad, fecha_registro)
                                VALUES (?, ?, ?, ?, ?)''',
                            (paciente.id_paciente, paciente.nombre, paciente.apellido,
                             paciente.edad, paciente.fecha_registro))
        self.conexion.commit()

    def agregar_imagen_paciente(self, id_paciente, ruta_imagen, fecha_toma):
        self.cursor.execute('''INSERT INTO imagenes 
                                (id_paciente, ruta, fecha_toma)
                                VALUES (?, ?, ?)''',
                            (id_paciente, ruta_imagen, fecha_toma))
        self.conexion.commit()

    def obtener_paciente(self, id_paciente):
        self.cursor.execute('''SELECT * FROM pacientes WHERE id = ?''', (id_paciente,))
        paciente_data = self.cursor.fetchone()
        if paciente_data:
            paciente = Paciente(*paciente_data)
            self.cursor.execute('''SELECT ruta, fecha_toma FROM imagenes 
                                    WHERE id_paciente = ?''', (id_paciente,))
            imagenes_data = self.cursor.fetchall()
            for imagen_data in imagenes_data:
                paciente.agregar_imagen(*imagen_data)
            return paciente
        else:
            return None

    def obtener_lista_pacientes(self):
        self.cursor.execute('''SELECT id FROM pacientes''')
        return [fila[0] for fila in self.cursor.fetchall()]

    def cerrar_conexion(self):
        self.conexion.close()

    @staticmethod
    def calcular_porcentaje_grasa(ruta_imagen):
        imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
        umbral, imagen_binaria = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY)
        total_pixeles = imagen.size
        pixeles_blancos = cv2.countNonZero(imagen_binaria)
        pixeles_negros = total_pixeles - pixeles_blancos
        porcentaje_grasa = (pixeles_negros / total_pixeles) * 100

        if porcentaje_grasa > 82:
            porcentaje_grasa = 20 + (porcentaje_grasa - 82) * 0.25
        elif porcentaje_grasa < 82:
            porcentaje_grasa = 2 + (porcentaje_grasa - 80) * 0.375
        if porcentaje_grasa < 0:
            porcentaje_grasa = 1

        return porcentaje_grasa
