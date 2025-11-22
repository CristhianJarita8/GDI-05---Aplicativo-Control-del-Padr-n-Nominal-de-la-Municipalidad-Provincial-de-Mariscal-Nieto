import tkinter as tk
from tkinter import ttk, messagebox


class BaseUI(tk.Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.geometry("900x600")

        # Frame para el formulario
        self.form_frame = tk.LabelFrame(self, text="Formulario", padx=10, pady=10)
        self.form_frame.pack(fill="x", padx=10, pady=10)

        # Frame para la tabla
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = None

    def crear_tabla(self, columnas):
        self.tree = ttk.Treeview(self.table_frame, columns=columnas, show="headings")

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(fill="both", expand=True)

    def mostrar_mensaje(self, texto, tipo="info"):
        if tipo == "info":
            messagebox.showinfo("Información", texto)
        else:
            messagebox.showerror("Error", texto)
