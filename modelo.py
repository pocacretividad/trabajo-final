import sqlite3

class BaseDeDatos:
    def __init__(self):
        self.conexion = sqlite3.connect("monitoreo_salud.db")
        self.crear_tablas()

    def crear_tablas(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            genero TEXT NOT NULL,
            diagnostico TEXT NOT NULL,
            fecha_registro TEXT NOT NULL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS mediciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            tipo_medicion TEXT NOT NULL,
            valor REAL NOT NULL,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
        )
        ''')
        self.conexion.commit()

    def agregar_paciente(self, nombre, edad, genero, diagnostico):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO pacientes (nombre, edad, genero, diagnostico, fecha_registro) VALUES (?, ?, ?, ?, datetime('now'))",
                       (nombre, edad, genero, diagnostico))
        self.conexion.commit()

    def obtener_pacientes(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT id, nombre, edad, diagnostico FROM pacientes")
        return cursor.fetchall()

    def agregar_medicion(self, paciente_id, tipo_medicion, valor):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO mediciones (paciente_id, fecha, tipo_medicion, valor) VALUES (?, datetime('now'), ?, ?)",
                       (paciente_id, tipo_medicion, valor))
        self.conexion.commit()

    def obtener_mediciones(self, paciente_id):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT fecha, tipo_medicion, valor FROM mediciones WHERE paciente_id = ?", (paciente_id,))
        return cursor.fetchall()

    
    def cerrar(self):
        self.conexion.close()