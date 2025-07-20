# archivo: modelo/gestor_db.py
import sqlite3
from sqlite3 import Error

class GestorDB:
    def __init__(self, db_file="data/clinica.db"):
        """
        Inicializa el gestor de la base de datos.
        Si db_file es None, usa una base de datos en memoria para las pruebas.
        """
        # Si no se especifica un archivo, usa ':memory:' para una BD temporal
        self.db_file = db_file if db_file is not None else ":memory:"
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_file)
            # Solo imprime el mensaje si no es una BD en memoria (para no ensuciar las pruebas)
            if self.db_file != ":memory:":
                print(f"Conexión exitosa a {self.db_file} (SQLite v{sqlite3.sqlite_version})")
        except Error as e:
            print(e)

    def crear_tablas(self):
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
            if self.db_file != ":memory:":
                print("Tablas creadas exitosamente.")
        except Error as e:
            print(f"Error al crear tablas: {e}")

    ### MÉTODOS PARA GESTIONAR PACIENTES ###
    def agregar_paciente(self, nombre, apellido, fecha_nacimiento, telefono):
        sql = ''' INSERT INTO pacientes(nombre, apellido, fecha_nacimiento, telefono)
                  VALUES(?,?,?,?) '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (nombre, apellido, fecha_nacimiento, telefono))
            self.conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al agregar paciente: {e}")
            return None

    def obtener_pacientes(self):
        sql = "SELECT * FROM pacientes"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener pacientes: {e}")
            return []

    def actualizar_paciente(self, id_paciente, nombre, apellido, fecha_nacimiento, telefono):
        sql = ''' UPDATE pacientes
                  SET nombre = ? ,
                      apellido = ? ,
                      fecha_nacimiento = ? ,
                      telefono = ?
                  WHERE id = ?'''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (nombre, apellido, fecha_nacimiento, telefono, id_paciente))
            self.conn.commit()
        except Error as e:
            print(f"Error al actualizar paciente: {e}")

    def eliminar_paciente(self, id_paciente):
        sql = 'DELETE FROM pacientes WHERE id = ?'
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (id_paciente,))
            self.conn.commit()
        except Error as e:
            print(f"Error al eliminar paciente: {e}")

    ### MÉTODOS PARA GESTIONAR MÉDICOS ###
    def agregar_medico(self, nombre, apellido, especialidad):
        sql = ''' INSERT INTO medicos(nombre, apellido, especialidad)
                  VALUES(?,?,?) '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (nombre, apellido, especialidad))
            self.conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al agregar médico: {e}")
            return None

    def obtener_medicos(self):
        sql = "SELECT * FROM medicos"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener médicos: {e}")
            return []

    def actualizar_medico(self, id_medico, nombre, apellido, especialidad):
        sql = ''' UPDATE medicos
                  SET nombre = ? ,
                      apellido = ? ,
                      especialidad = ?
                  WHERE id = ?'''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (nombre, apellido, especialidad, id_medico))
            self.conn.commit()
        except Error as e:
            print(f"Error al actualizar médico: {e}")

    def eliminar_medico(self, id_medico):
        sql = 'DELETE FROM medicos WHERE id = ?'
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (id_medico,))
            self.conn.commit()
        except Error as e:
            print(f"Error al eliminar médico: {e}")
            
    ### MÉTODOS PARA GESTIONAR CITAS ###
    def agendar_cita(self, paciente_id, medico_id, fecha_hora, motivo):
        sql = ''' INSERT INTO citas(paciente_id, medico_id, fecha_hora, motivo, estado)
                  VALUES(?,?,?,?,'Programada') '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (paciente_id, medico_id, fecha_hora, motivo))
            self.conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al agendar cita: {e}")
            return None

    def obtener_citas_detalladas(self):
        sql = """
            SELECT
                c.id,
                p.nombre || ' ' || p.apellido AS nombre_paciente,
                m.nombre || ' ' || m.apellido AS nombre_medico,
                c.fecha_hora,
                c.motivo,
                c.estado
            FROM citas c
            JOIN pacientes p ON c.paciente_id = p.id
            JOIN medicos m ON c.medico_id = m.id
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener citas detalladas: {e}")
            return []

    def actualizar_cita(self, id_cita, paciente_id, medico_id, fecha_hora, motivo):
        sql = ''' UPDATE citas
                  SET paciente_id = ?,
                      medico_id = ?,
                      fecha_hora = ?,
                      motivo = ?
                  WHERE id = ?'''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (paciente_id, medico_id, fecha_hora, motivo, id_cita))
            self.conn.commit()
        except Error as e:
            print(f"Error al actualizar cita: {e}")
            
    def cambiar_estado_cita(self, id_cita, nuevo_estado):
        sql = "UPDATE citas SET estado = ? WHERE id = ?"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (nuevo_estado, id_cita))
            self.conn.commit()
        except Error as e:
            print(f"Error al cambiar estado de la cita: {e}")

    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()
            # No imprimimos mensaje aquí para mantener limpias las pruebas