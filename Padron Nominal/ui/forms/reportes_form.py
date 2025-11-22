import tkinter as tk
from tkinter import ttk
import mysql.connector

from ui.theme import PALETTE, load_icon
from db.connection import DatabaseConnection 


class ReportesForm(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Reportes")
        self.geometry("900x600")
        self.configure(bg=PALETTE["bg"])

        # instancia de tu conexión centralizada
        self.db = DatabaseConnection()

        tk.Label(self, text="GENERADOR DE REPORTES",
                 bg=PALETTE["bg"], fg="white",
                 font=("Segoe UI", 16, "bold")).pack(pady=10)

        cont = tk.Frame(self, bg=PALETTE["bg"])
        cont.pack(pady=10)

        tk.Label(cont, text="Seleccione reporte:",
                 bg=PALETTE["bg"], fg="white",
                 font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)

        self.reportes = {
            "Mostrar todos los infantes": "sp_mostrar_infantes",
            "Infantes y sus fechas de visita": "sp_infantes_visitas",
            "Infantes nacidos en 2024": "sp_infantes_nacidos_2024",
            "Apoderados con grado Superior": "sp_apoderados_superior",
            "Promedio de peso de infantes": "sp_promedio_peso",
            "Infantes y su distrito de visita": "sp_infantes_distrito",
            "Relación Apoderados - Infantes": "sp_apoderados_infantes",
            "Contar infantes por distrito": "sp_contar_infantes_distrito",
            "Infantes con anemia": "sp_infantes_anemia",
            "Infantes con establecimiento de salud": "sp_infantes_establecimiento",
            "Total de infantes con CRED completo": "sp_total_cred",
            "Infantes por establecimiento de salud": "sp_infantes_por_establecimiento",
        }

        self.combo = ttk.Combobox(cont,
                                  values=list(self.reportes.keys()),
                                  width=45,
                                  font=("Segoe UI", 11))
        self.combo.pack(side="left", padx=10)
        self.combo.current(0)

        icon_search = load_icon("search", size=18)
        tk.Button(cont, text=" Generar", image=icon_search, compound="left",
                  bg=PALETTE["primary"], fg="white",
                  font=("Segoe UI", 11, "bold"), bd=0,
                  command=self.generar_reporte).pack(side="left", padx=10)

        self.icon_search = icon_search  # Evitar GC

        self.tabla = ttk.Treeview(self)
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def generar_reporte(self):
        nombre = self.combo.get()
        procedimiento = self.reportes[nombre]

        try:
            conn = self.db.get_connection()   # ← tu conexión real
            cursor = conn.cursor()

            cursor.callproc(procedimiento)

            for result in cursor.stored_results():
                datos = result.fetchall()
                columnas = result.column_names

            # limpiar tabla
            self.tabla.delete(*self.tabla.get_children())
            self.tabla["columns"] = columnas
            self.tabla["show"] = "headings"

            for col in columnas:
                self.tabla.heading(col, text=col)
                self.tabla.column(col, width=150, anchor="center")

            for fila in datos:
                self.tabla.insert("", "end", values=fila)

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error en MySQL:", err)
