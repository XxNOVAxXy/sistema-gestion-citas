# archivo: main.py
import tkinter as tk
from tkinter import messagebox
from modelo.gestor_db import GestorDB

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Citas Médicas")
        self.geometry("500x300")
        
        # Inicializar gestor de BD y crear tablas
        self.gestor_db = GestorDB()
        self.gestor_db.crear_tablas()

        self.inicializar_componentes()
        
        # Asegurarse de cerrar la conexión al cerrar la ventana
        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def inicializar_componentes(self):
        # Contenedor principal
        main_frame = tk.Frame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título
        label_titulo = tk.Label(main_frame, text="Menú Principal", font=("Arial", 20, "bold"))
        label_titulo.pack(pady=10)

        # Botones del menú
        btn_pacientes = tk.Button(main_frame, text="Gestionar Pacientes", command=self.abrir_gestion_pacientes, width=30, height=2)
        btn_pacientes.pack(pady=10)

        btn_medicos = tk.Button(main_frame, text="Gestionar Médicos", command=self.abrir_gestion_medicos, width=30, height=2)
        btn_medicos.pack(pady=10)

        btn_citas = tk.Button(main_frame, text="Gestionar Citas", command=self.abrir_gestion_citas, width=30, height=2)
        btn_citas.pack(pady=10)

    def abrir_gestion_pacientes(self):
        messagebox.showinfo("Información", "Función para gestionar pacientes aún no implementada.")

    def abrir_gestion_medicos(self):
        messagebox.showinfo("Información", "Función para gestionar médicos aún no implementada.")

    def abrir_gestion_citas(self):
        messagebox.showinfo("Información", "Función para gestionar citas aún no implementada.")
        
    def cerrar_aplicacion(self):
        self.gestor_db.cerrar_conexion()
        self.destroy()

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()