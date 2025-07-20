# archivo: gui/ventana_medicos.py
import tkinter as tk
from tkinter import ttk, messagebox

class VentanaMedicos(tk.Toplevel):
    def __init__(self, parent, gestor_db):
        super().__init__(parent)
        self.parent = parent
        self.gestor_db = gestor_db
        self.selected_id = None

        self.title("Gestión de Médicos")
        self.geometry("700x450")
        
        panel_izquierdo = tk.Frame(self)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        panel_derecho = tk.Frame(self)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(panel_izquierdo, text="Formulario de Médico", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(panel_izquierdo, text="Nombre:").pack(anchor="w")
        self.entry_nombre = tk.Entry(panel_izquierdo, width=30)
        self.entry_nombre.pack(pady=5)
        
        tk.Label(panel_izquierdo, text="Apellido:").pack(anchor="w")
        self.entry_apellido = tk.Entry(panel_izquierdo, width=30)
        self.entry_apellido.pack(pady=5)
        
        tk.Label(panel_izquierdo, text="Especialidad:").pack(anchor="w")
        self.entry_especialidad = tk.Entry(panel_izquierdo, width=30)
        self.entry_especialidad.pack(pady=5)
        
        frame_botones = tk.Frame(panel_izquierdo)
        frame_botones.pack(pady=20)
        
        tk.Button(frame_botones, text="Agregar", command=self.agregar_medico).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Actualizar", command=self.actualizar_medico).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Eliminar", command=self.eliminar_medico).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame_botones, text="Limpiar", command=self.limpiar_formulario).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(panel_derecho, text="Lista de Médicos", font=("Arial", 16)).pack(pady=10)
        
        self.tree = ttk.Treeview(panel_derecho, columns=("ID", "Nombre", "Apellido", "Especialidad"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Especialidad", text="Especialidad")
        
        self.tree.column("ID", width=30, anchor="center")
        self.tree.column("Nombre", width=120)
        self.tree.column("Apellido", width=120)
        self.tree.column("Especialidad", width=120)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_medico)

        self.actualizar_lista_medicos()

    def actualizar_lista_medicos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for medico in self.gestor_db.obtener_medicos():
            self.tree.insert("", "end", values=medico)

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_especialidad.delete(0, tk.END)
        self.selected_id = None
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection()[0])

    def agregar_medico(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        especialidad = self.entry_especialidad.get()
        
        if nombre and apellido and especialidad:
            self.gestor_db.agregar_medico(nombre, apellido, especialidad)
            messagebox.showinfo("Éxito", "Médico agregado correctamente")
            self.limpiar_formulario()
            self.actualizar_lista_medicos()
        else:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")

    ### MÉTODO CORREGIDO ###
    def seleccionar_medico(self, event):
        selected_item = self.tree.selection()
        if not selected_item: return
            
        medico = self.tree.item(selected_item[0])['values']
        self.selected_id = medico[0]
        
        # Limpiamos los campos manualmente aquí
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_especialidad.delete(0, tk.END)
        # Y luego los rellenamos
        self.entry_nombre.insert(0, medico[1])
        self.entry_apellido.insert(0, medico[2])
        self.entry_especialidad.insert(0, medico[3])

    def actualizar_medico(self):
        if self.selected_id is None:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un médico de la lista.")
            return

        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        especialidad = self.entry_especialidad.get()

        if nombre and apellido and especialidad:
            self.gestor_db.actualizar_medico(self.selected_id, nombre, apellido, especialidad)
            messagebox.showinfo("Éxito", "Médico actualizado correctamente")
            self.limpiar_formulario()
            self.actualizar_lista_medicos()
        else:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
    
    def eliminar_medico(self):
        if self.selected_id is None:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un médico de la lista.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar a este médico?"):
            self.gestor_db.eliminar_medico(self.selected_id)
            messagebox.showinfo("Éxito", "Médico eliminado correctamente")
            self.limpiar_formulario()
            self.actualizar_lista_medicos()