import sqlite3
import os
from datetime import datetime
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

    def calcular_grasa_higado(self):
        grasa_total = 0
        for ruta_imagen, _ in self.imagenes:
            imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
            _, binarizada = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY)
            porcentaje_grasa = np.count_nonzero(binarizada) / (binarizada.shape[0] * binarizada.shape[1]) * 100
            grasa_total += porcentaje_grasa
        return grasa_total / len(self.imagenes) if len(self.imagenes) > 0 else 0

class BaseDatos:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()

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
                                fecha_toma TEXT
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

# Inicializar la base de datos
if not os.path.exists('pacientes.db'):
    db = BaseDatos('pacientes.db')
    db.crear_tabla_pacientes()
    db.crear_tabla_imagenes()
    db.cerrar_conexion()
