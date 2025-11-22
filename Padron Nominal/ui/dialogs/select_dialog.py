import tkinter as tk
from tkinter import ttk, messagebox

class SelectDialog(tk.Toplevel):
    def __init__(self, parent, pk_columns):
        super().__init__(parent)
        self.title("Seleccionar registro")
        self.pk_columns = pk_columns
        self.values = {}

        self.vars = {pk: tk.StringVar() for pk in pk_columns}

        for i, pk in enumerate(pk_columns):
            ttk.Label(self, text=pk).grid(row=i, column=0, padx=6, pady=4, sticky="w")
            ttk.Entry(self, textvariable=self.vars[pk]).grid(row=i, column=1, padx=6, pady=4)

        ttk.Button(self, text="Aceptar", command=self.accept).grid(row=len(pk_columns), column=0, pady=10)
        ttk.Button(self, text="Cancelar", command=self.destroy).grid(row=len(pk_columns), column=1, pady=10)

        self.grab_set()

    def accept(self):
        self.values = {pk: self.vars[pk].get().strip() for pk in self.pk_columns}
        if not all(self.values.values()):
            messagebox.showwarning("Validación", "Complete todos los campos clave.")
            return
        self.destroy()
