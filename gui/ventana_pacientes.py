# archivo: gui/ventana_pacientes.py
import tkinter as tk
from tkinter import ttk, messagebox

class VentanaPacientes(tk.Toplevel):
    def __init__(self, parent, gestor_db):
        super().__init__(parent)
        self.parent = parent
        self.gestor_db = gestor_db
        self.selected_id = None

        self.title("Gestión de Pacientes")
        self.geometry("800x500")
        
        panel_izquierdo = tk.Frame(self)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        panel_derecho = tk.Frame(self)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(panel_izquierdo, text="Formulario de Paciente", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(panel_izquierdo, text="Nombre:").pack(anchor="w")
        self.entry_nombre = tk.Entry(panel_izquierdo, width=30)
        self.entry_nombre.pack(pady=5)
        
        tk.Label(panel_izquierdo, text="Apellido:").pack(anchor="w")
        self.entry_apellido = tk.Entry(panel_izquierdo, width=30)
        self.entry_apellido.pack(pady=5)
        
        tk.Label(panel_izquierdo, text="Fecha de Nacimiento (YYYY-MM-DD):").pack(anchor="w")
        self.entry_fecha_nac = tk.Entry(panel_izquierdo, width=30)
        self.entry_fecha_nac.pack(pady=5)
        
        tk.Label(panel_izquierdo, text="Teléfono:").pack(anchor="w")
        self.entry_telefono = tk.Entry(panel_izquierdo, width=30)
        self.entry_telefono.pack(pady=5)
        
        frame_botones = tk.Frame(panel_izquierdo)
        frame_botones.pack(pady=20)
        
        tk.Button(frame_botones, text="Agregar", command=self.agregar_paciente).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Actualizar", command=self.actualizar_paciente).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Eliminar", command=self.eliminar_paciente).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame_botones, text="Limpiar", command=self.limpiar_formulario).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(panel_derecho, text="Lista de Pacientes", font=("Arial", 16)).pack(pady=10)
        
        self.tree = ttk.Treeview(panel_derecho, columns=("ID", "Nombre", "Apellido", "Teléfono"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Teléfono", text="Teléfono")
        
        self.tree.column("ID", width=30, anchor="center")
        self.tree.column("Nombre", width=120)
        self.tree.column("Apellido", width=120)
        self.tree.column("Teléfono", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_paciente)

        self.actualizar_lista_pacientes()

    def actualizar_lista_pacientes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        pacientes = self.gestor_db.obtener_pacientes()
        for p in pacientes:
            self.tree.insert("", "end", values=(p[0], p[1], p[2], p[4]))

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_fecha_nac.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.selected_id = None
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection()[0])

    def agregar_paciente(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        fecha_nac = self.entry_fecha_nac.get()
        telefono = self.entry_telefono.get()
        
        if nombre and apellido and telefono:
            self.gestor_db.agregar_paciente(nombre, apellido, fecha_nac, telefono)
            messagebox.showinfo("Éxito", "Paciente agregado correctamente")
            self.limpiar_formulario()
            self.actualizar_lista_pacientes()
        else:
            messagebox.showwarning("Campos vacíos", "Nombre, Apellido y Teléfono son obligatorios.")

    ### MÉTODO CORREGIDO ###
    def seleccionar_paciente(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
            
        paciente_fila = self.tree.item(selected_item[0])['values']
        self.selected_id = paciente_fila[0]

        pacientes = self.gestor_db.obtener_pacientes()
        paciente_completo = next((p for p in pacientes if p[0] == self.selected_id), None)
        
        if paciente_completo:
            # Limpiamos los campos manualmente aquí
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
            self.entry_fecha_nac.delete(0, tk.END)
            self.entry_telefono.delete(0, tk.END)
            # Y luego los rellenamos
            self.entry_nombre.insert(0, paciente_completo[1])
            self.entry_apellido.insert(0, paciente_completo[2])
            self.entry_fecha_nac.insert(0, paciente_completo[3] or "")
            self.entry_telefono.insert(0, paciente_completo[4])

    def actualizar_paciente(self):
        if self.selected_id is None:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un paciente de la lista para actualizar.")
            return

        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        fecha_nac = self.entry_fecha_nac.get()
        telefono = self.entry_telefono.get()

        if nombre and apellido and telefono:
            self.gestor_db.actualizar_paciente(self.selected_id, nombre, apellido, fecha_nac, telefono)
            messagebox.showinfo("Éxito", "Paciente actualizado correctamente")
            self.limpiar_formulario()
            self.actualizar_lista_pacientes()
        else:
            messagebox.showwarning("Campos vacíos", "Nombre, Apellido y Teléfono son obligatorios.")
    
    def eliminar_paciente(self):
        if self.selected_id is None:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un paciente de la lista para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este paciente?"):
            self.gestor_db.eliminar_paciente(self.selected_id)
            messagebox.showinfo("Éxito", "Paciente eliminado correctamente")
            self.limpiar_formulario()
            self.actualizar_lista_pacientes()