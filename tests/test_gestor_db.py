# archivo: tests/test_gestor_db.py
import unittest
import sys
import os

# Añadimos la ruta del directorio principal al path de Python
# para que pueda encontrar el módulo 'modelo'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modelo.gestor_db import GestorDB

class TestGestorDB(unittest.TestCase):

    def setUp(self):
        """
        Este método se ejecuta ANTES de cada prueba.
        Crea una nueva base de datos en memoria y las tablas para cada prueba.
        """
        # Usamos None para indicar que queremos una BD en memoria
        self.gestor = GestorDB(db_file=None) 
        self.gestor.crear_tablas()
        print("\nEjecutando prueba:", self._testMethodName)

    def tearDown(self):
        """
        Este método se ejecuta DESPUÉS de cada prueba.
        Cierra la conexión a la base de datos.
        """
        self.gestor.cerrar_conexion()
        print("Prueba finalizada.")

    # --- NUESTRAS 3 FUNCIONES DE PRUEBA ---

    def test_agregar_paciente(self):
        """ Prueba que se puede agregar un paciente correctamente. """
        print("-> Probando agregar_paciente...")
        paciente_id = self.gestor.agregar_paciente("Juan", "Perez", "1990-05-15", "123456789")
        
        # assertIsNotNone comprueba que el ID devuelto no sea nulo (lo que indicaría un error)
        self.assertIsNotNone(paciente_id, "El ID del paciente no debería ser nulo tras la inserción.")
        
        # Comprobamos que el paciente realmente está en la base de datos
        pacientes = self.gestor.obtener_pacientes()
        self.assertEqual(len(pacientes), 1, "Debería haber exactamente 1 paciente en la BD.")
        self.assertEqual(pacientes[0][1], "Juan", "El nombre del paciente no coincide.")

    def test_agregar_medico(self):
        """ Prueba que se puede agregar un médico correctamente. """
        print("-> Probando agregar_medico...")
        medico_id = self.gestor.agregar_medico("Ana", "Gomez", "Cardiología")

        self.assertIsNotNone(medico_id)
        
        medicos = self.gestor.obtener_medicos()
        self.assertEqual(len(medicos), 1)
        self.assertEqual(medicos[0][3], "Cardiología", "La especialidad del médico no coincide.")

    def test_agendar_cita(self):
        """ Prueba que se puede agendar una cita correctamente. """
        print("-> Probando agendar_cita...")
        # Primero necesitamos un paciente y un médico
        paciente_id = self.gestor.agregar_paciente("Carlos", "Lopez", "1985-11-20", "987654321")
        medico_id = self.gestor.agregar_medico("Lucia", "Martinez", "Pediatría")

        # Ahora agendamos la cita
        cita_id = self.gestor.agendar_cita(paciente_id, medico_id, "2025-08-01 10:30", "Revisión anual")

        self.assertIsNotNone(cita_id)
        
        # Usamos el nuevo método para obtener citas detalladas
        citas = self.gestor.obtener_citas_detalladas()
        self.assertEqual(len(citas), 1)
        # Verificamos que el nombre del paciente en la cita sea el correcto
        self.assertEqual(citas[0][1], "Carlos Lopez", "El nombre del paciente en la cita no coincide.")

# Esto permite ejecutar las pruebas directamente desde la línea de comandos
if __name__ == '__main__':
    unittest.main()