import tkinter as tk
from tkinter import ttk

class ConfirmDialog(tk.Toplevel):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.title("Confirmar acción")

        ttk.Label(self, text=message).pack(padx=10, pady=10)

        self.response = False

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Sí", command=self.accept).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="No", command=self.reject).grid(row=0, column=1, padx=5)

        self.grab_set()

    def accept(self):
        self.response = True
        self.destroy()

    def reject(self):
        self.response = False
        self.destroy()
