# archivo: gui/ventana_citas.py
import tkinter as tk
from tkinter import ttk, messagebox

class VentanaCitas(tk.Toplevel):
    def __init__(self, parent, gestor_db):
        super().__init__(parent)
        self.parent = parent
        self.gestor_db = gestor_db
        self.pacientes = self.gestor_db.obtener_pacientes()
        self.medicos = self.gestor_db.obtener_medicos()
        self.selected_id = None

        self.title("Gestión de Citas")
        self.geometry("950x550")
        
        panel_izquierdo = tk.Frame(self)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        panel_derecho = tk.Frame(self)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(panel_izquierdo, text="Formulario de Cita", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(panel_izquierdo, text="Paciente:").pack(anchor="w")
        self.combo_pacientes = ttk.Combobox(panel_izquierdo, width=35, state="readonly")
        self.combo_pacientes['values'] = [f"{p[1]} {p[2]} (ID: {p[0]})" for p in self.pacientes]
        self.combo_pacientes.pack(pady=5)
        
        tk.Label(panel_izquierdo, text="Médico:").pack(anchor="w")
        self.combo_medicos = ttk.Combobox(panel_izquierdo, width=35, state="readonly")
        self.combo_medicos['values'] = [f"{m[1]} {m[2]} - {m[3]} (ID: {m[0]})" for m in self.medicos]
        self.combo_medicos.pack(pady=5)
        
        tk.Label(panel_izquierdo, text="Fecha y Hora (YYYY-MM-DD HH:MM):").pack(anchor="w")
        self.entry_fecha = tk.Entry(panel_izquierdo, width=38)
        self.entry_fecha.pack(pady=5)

        tk.Label(panel_izquierdo, text="Motivo de la consulta:").pack(anchor="w")
        self.entry_motivo = tk.Text(panel_izquierdo, width=38, height=5)
        self.entry_motivo.pack(pady=5)
        
        frame_botones = tk.Frame(panel_izquierdo)
        frame_botones.pack(pady=20)
        
        tk.Button(frame_botones, text="Agendar", command=self.agendar_cita).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Reprogramar", command=self.reprogramar_cita).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Cancelar Cita", command=self.cancelar_cita).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame_botones, text="Limpiar", command=self.limpiar_formulario).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(panel_derecho, text="Citas Programadas", font=("Arial", 16)).pack(pady=10)
        
        self.tree = ttk.Treeview(panel_derecho, columns=("ID", "Paciente", "Médico", "Fecha/Hora", "Motivo", "Estado"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Paciente", text="Paciente")
        self.tree.heading("Médico", text="Médico")
        self.tree.heading("Fecha/Hora", text="Fecha/Hora")
        self.tree.heading("Motivo", text="Motivo")
        self.tree.heading("Estado", text="Estado")
        
        self.tree.column("ID", width=30, anchor="center")
        self.tree.column("Paciente", width=150)
        self.tree.column("Médico", width=150)
        self.tree.column("Fecha/Hora", width=120)
        self.tree.column("Motivo", width=150)
        self.tree.column("Estado", width=80, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_cita)

        self.actualizar_lista_citas()

    def _get_id_from_combobox(self, combo_value):
        try:
            return int(combo_value.split('(ID: ')[1].replace(')', ''))
        except (IndexError, ValueError, AttributeError):
            return None

    def actualizar_lista_citas(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for cita in self.gestor_db.obtener_citas_detalladas():
            self.tree.insert("", "end", values=cita)

    def limpiar_formulario(self):
        self.combo_pacientes.set('')
        self.combo_medicos.set('')
        self.entry_fecha.delete(0, tk.END)
        self.entry_motivo.delete('1.0', tk.END)
        self.selected_id = None
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection()[0])

    def agendar_cita(self):
        paciente_val = self.combo_pacientes.get()
        medico_val = self.combo_medicos.get()
        fecha_hora = self.entry_fecha.get()
        motivo = self.entry_motivo.get('1.0', tk.END).strip()

        paciente_id = self._get_id_from_combobox(paciente_val)
        medico_id = self._get_id_from_combobox(medico_val)

        if paciente_id and medico_id and fecha_hora:
            self.gestor_db.agendar_cita(paciente_id, medico_id, fecha_hora, motivo)
            messagebox.showinfo("Éxito", "Cita agendada correctamente")
            self.limpiar_formulario()
            self.actualizar_lista_citas()
        else:
            messagebox.showwarning("Campos incompletos", "Debe seleccionar un paciente, un médico e ingresar la fecha.")

    ### MÉTODO CORREGIDO ###
    def seleccionar_cita(self, event):
        selected_item = self.tree.selection()
        if not selected_item: return
        
        cita = self.tree.item(selected_item[0])['values']
        self.selected_id = cita[0]
        
        # Limpiamos los campos manualmente aquí
        self.combo_pacientes.set('')
        self.combo_medicos.set('')
        self.entry_fecha.delete(0, tk.END)
        self.entry_motivo.delete('1.0', tk.END)
        
        # Y luego los rellenamos
        paciente_val = next((p_val for p_val in self.combo_pacientes['values'] if cita[1] in p_val), None)
        if paciente_val: self.combo_pacientes.set(paciente_val)

        medico_val = next((m_val for m_val in self.combo_medicos['values'] if cita[2] in m_val), None)
        if medico_val: self.combo_medicos.set(medico_val)
        
        self.entry_fecha.insert(0, cita[3])
        self.entry_motivo.insert('1.0', cita[4])

    def reprogramar_cita(self):
        if self.selected_id is None:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione una cita de la lista para reprogramar.")
            return

        paciente_id = self._get_id_from_combobox(self.combo_pacientes.get())
        medico_id = self._get_id_from_combobox(self.combo_medicos.get())
        fecha_hora = self.entry_fecha.get()
        motivo = self.entry_motivo.get('1.0', tk.END).strip()

        if paciente_id and medico_id and fecha_hora:
            self.gestor_db.actualizar_cita(self.selected_id, paciente_id, medico_id, fecha_hora, motivo)
            messagebox.showinfo("Éxito", "Cita reprogramada correctamente")
            self.limpiar_formulario()
            self.actualizar_lista_citas()
        else:
            messagebox.showwarning("Campos incompletos", "Debe seleccionar un paciente, un médico e ingresar la fecha.")

    def cancelar_cita(self):
        if self.selected_id is None:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione una cita de la lista para cancelar.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea CANCELAR esta cita?"):
            self.gestor_db.cambiar_estado_cita(self.selected_id, "Cancelada")
            messagebox.showinfo("Éxito", "La cita ha sido cancelada")
            self.limpiar_formulario()
            self.actualizar_lista_citas()