import tkinter as tk
from tkinter import ttk, messagebox
from ui.dialogs.select_dialog import SelectDialog
from ui.dialogs.confirm_dialog import ConfirmDialog
from db.services.infante_service import InfanteService
from ui.theme import IconButton, load_icon, PALETTE


class InfanteForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Infantes")
        self.geometry("850x520")
        self.service = InfanteService()

        labels = [
            ("DNI_CE", 0), ("Codigo_PadronNominal", 1),
            ("Nombre_Infante", 2), ("Apellido_Paterno", 3),
            ("Apellido_Materno", 4), ("FechaNacimiento_Infante (YYYY-MM-DD)", 5),
            ("Codigo_Sexo", 6)
        ]
        self.vars = {}
        for text, idx in labels:
            ttk.Label(self, text=text).grid(row=idx, column=0, padx=6, pady=4, sticky="w")
            v = tk.StringVar()
            ttk.Entry(self, textvariable=v, width=30).grid(row=idx, column=1, padx=6, pady=4, sticky="w")
            self.vars[text] = v

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=0, column=2, rowspan=4, padx=12, pady=6, sticky="n")

        IconButton(
            btn_frame,
            icon_name="add",
            text="Insertar",
            command=self.insertar
        ).grid(row=0, column=0, pady=6, sticky="ew")

        IconButton(
            btn_frame,
            icon_name="edit",
            text="Cargar (para modificar)",
            command=self.cargar_para_modificar
        ).grid(row=1, column=0, pady=6, sticky="ew")

        IconButton(
            btn_frame,
            icon_name="refresh",
            text="Actualizar",
            command=self.actualizar
        ).grid(row=2, column=0, pady=6, sticky="ew")

        IconButton(
            btn_frame,
            icon_name="delete",
            text="Eliminar",
            command=self.eliminar
        ).grid(row=3, column=0, pady=6, sticky="ew")

        IconButton(
            btn_frame,
            icon_name="refresh",
            text="Refrescar lista",
            command=self.refrescar_lista
        ).grid(row=4, column=0, pady=6, sticky="ew")


        cols = ["DNI_CE","Codigo_PadronNominal","Nombre_Infante","Apellido_Paterno","Apellido_Materno","FechaNacimiento_Infante","Codigo_Sexo"]
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="w")
        self.tree.grid(row=8, column=0, columnspan=3, padx=6, pady=10, sticky="nsew")
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.grid(row=8, column=3, sticky="ns")

        self.grid_rowconfigure(8, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.refrescar_lista()

    def _read_form(self):
        return (
            self.vars["DNI_CE"].get().strip(),
            self.vars["Codigo_PadronNominal"].get().strip(),
            self.vars["Nombre_Infante"].get().strip(),
            self.vars["Apellido_Paterno"].get().strip(),
            self.vars["Apellido_Materno"].get().strip(),
            self.vars["FechaNacimiento_Infante (YYYY-MM-DD)"].get().strip(),
            self.vars["Codigo_Sexo"].get().strip()
        )

    def insertar(self):
        data = self._read_form()
        if not all(data):
            messagebox.showwarning("Validación", "Complete todos los campos antes de insertar.")
            return
        try:
            self.service.crear(data)
            messagebox.showinfo("Éxito", "Infante insertado.")
            self.refrescar_lista()
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))

    def refrescar_lista(self):
        try:
            rows = self.service.listar()
            for it in self.tree.get_children():
                self.tree.delete(it)
            for r in rows:
                values = [r.get(c) for c in self.tree["columns"]]
                self.tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("Error al listar", str(e))

    def cargar_para_modificar(self):
        dlg = SelectDialog(self, ["DNI_CE", "Codigo_PadronNominal"])
        self.wait_window(dlg)
        if not getattr(dlg, "values", None):
            return
        pk = dlg.values
        try:
            row = self.service.get_by_pk(pk["DNI_CE"], pk["Codigo_PadronNominal"])
            if not row:
                messagebox.showinfo("No encontrado", "No hay registro con esas claves.")
                return
            self.vars["DNI_CE"].set(row.get("DNI_CE") or "")
            self.vars["Codigo_PadronNominal"].set(row.get("Codigo_PadronNominal") or "")
            self.vars["Nombre_Infante"].set(row.get("Nombre_Infante") or "")
            self.vars["Apellido_Paterno"].set(row.get("Apellido_Paterno") or "")
            self.vars["Apellido_Materno"].set(row.get("Apellido_Materno") or "")
            # fecha safe formatting
            self.vars["FechaNacimiento_Infante (YYYY-MM-DD)"].set((row.get("FechaNacimiento_Infante") or "").strftime("%Y-%m-%d") if getattr(row.get("FechaNacimiento_Infante"), "strftime", None) else (row.get("FechaNacimiento_Infante") or ""))
            self.vars["Codigo_Sexo"].set(row.get("Codigo_Sexo") or "")
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))

    def actualizar(self):
        data = self._read_form()
        if not (data[0] and data[1]):
            messagebox.showwarning("PK faltante", "DNI_CE y Codigo_PadronNominal son obligatorios para actualizar.")
            return
        try:
            self.service.modificar(data)
            messagebox.showinfo("Éxito", "Infante actualizado.")
            self.refrescar_lista()
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))

    def eliminar(self):
        dlg = SelectDialog(self, ["DNI_CE", "Codigo_PadronNominal"])
        self.wait_window(dlg)
        if not getattr(dlg, "values", None):
            return
        pk = dlg.values
        confirm = ConfirmDialog(self, f"¿Eliminar infante {pk}?")
        self.wait_window(confirm)
        if not getattr(confirm, "response", False):
            return
        try:
            self.service.eliminar(pk["DNI_CE"], pk["Codigo_PadronNominal"])
            messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")
            self.refrescar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))

    def _clear_form(self):
        for v in self.vars.values():
            v.set("")
