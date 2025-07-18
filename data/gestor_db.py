# archivo: modelo/gestor_db.py
import sqlite3
from sqlite3 import Error

class GestorDB:
    def __init__(self, db_file="data/clinica.db"):
        """
        Inicializa el gestor de la base de datos.
        :param db_file: ruta al archivo de la base de datos.
        """
        self.db_file = db_file
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(f"Conexión exitosa a {self.db_file} (SQLite v{sqlite3.sqlite_version})")
        except Error as e:
            print(e)

    def crear_tablas(self):
        """ Crea las tablas necesarias en la base de datos si no existen. """
        sql_tabla_pacientes = """
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            fecha_nacimiento TEXT,
            telefono TEXT UNIQUE
        );
        """

        sql_tabla_medicos = """
        CREATE TABLE IF NOT EXISTS medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            especialidad TEXT NOT NULL
        );
        """

        sql_tabla_citas = """
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            medico_id INTEGER NOT NULL,
            fecha_hora TEXT NOT NULL,
            motivo TEXT,
            estado TEXT DEFAULT 'Programada',
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (medico_id) REFERENCES medicos (id)
        );
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_tabla_pacientes)
            cursor.execute(sql_tabla_medicos)
            cursor.execute(sql_tabla_citas)
            self.conn.commit()
            print("Tablas creadas exitosamente.")
        except Error as e:
            print(f"Error al crear tablas: {e}")

    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada.")

# Código para probar la creación de tablas
if __name__ == '__main__':
    gestor = GestorDB()
    gestor.crear_tablas()
    gestor.cerrar_conexion()