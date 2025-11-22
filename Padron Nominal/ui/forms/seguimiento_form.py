import tkinter as tk
from tkinter import ttk, messagebox
from ui.dialogs.select_dialog import SelectDialog
from ui.dialogs.confirm_dialog import ConfirmDialog
from db.services.seguimientoNominal_service import SeguimientoNominalService
from ui.theme import IconButton

class SeguimientoForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Seguimiento_Nominal")
        self.geometry("900x520")
        self.service = SeguimientoNominalService()

        labels = [
            ("ID_SeguimientoNominal",0),("EstablecimientoSalud",1),("Fecha",2),("Observaciones",3),("ID_HomologacionNominal",4)
        ]
        self.vars = {}
        for text, idx in labels:
            ttk.Label(self, text=text).grid(row=idx, column=0, padx=6, pady=4, sticky="w")
            v = tk.StringVar()
            ttk.Entry(self, textvariable=v, width=35).grid(row=idx, column=1, padx=6, pady=4, sticky="w")
            self.vars[text] = v

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=0, column=3, rowspan=6, padx=12, pady=6, sticky="n")

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


        cols = ["ID_SeguimientoNominal","EstablecimientoSalud","Fecha","Observaciones","ID_HomologacionNominal"]
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=160, anchor="w")
        self.tree.grid(row=8, column=0, columnspan=3, padx=6, pady=10, sticky="nsew")
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.grid(row=8, column=3, sticky="ns")

        self.grid_rowconfigure(8, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.refrescar_lista()

    def _read_form(self):
        return (
            self.vars["ID_SeguimientoNominal"].get().strip(),
            self.vars["EstablecimientoSalud"].get().strip(),
            self.vars["Fecha"].get().strip(),
            self.vars["Observaciones"].get().strip(),
            self.vars["ID_HomologacionNominal"].get().strip()
        )

    def insertar(self):
        data = self._read_form()
        if not all(data):
            messagebox.showwarning("Validación", "Complete todos los campos antes de insertar.")
            return
        try:
            self.service.crear(data)
            messagebox.showinfo("Éxito", "Seguimiento_Nominal insertado.")
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
        dlg = SelectDialog(self, ["ID_SeguimientoNominal"])
        self.wait_window(dlg)
        if not getattr(dlg, "values", None):
            return
        pk = dlg.values
        try:
            row = self.service.get_by_pk(pk["ID_SeguimientoNominal"])
            if not row:
                messagebox.showinfo("No encontrado", "No hay registro con esas claves.")
                return
            self.vars["ID_SeguimientoNominal"].set(row.get("ID_SeguimientoNominal") or "")
            self.vars["EstablecimientoSalud"].set(row.get("EstablecimientoSalud") or "")
            self.vars["Fecha"].set((row.get("Fecha") or "").strftime("%Y-%m-%d") if getattr(row.get("Fecha"), "strftime", None) else (row.get("Fecha") or ""))
            self.vars["Observaciones"].set(row.get("Observaciones") or "")
            self.vars["ID_HomologacionNominal"].set(row.get("ID_HomologacionNominal") or "")
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))

    def actualizar(self):
        data = self._read_form()
        if not (data[0]):
            messagebox.showwarning("PK faltante", "ID_SeguimientoNominal es obligatorio para actualizar.")
            return
        try:
            self.service.modificar(data)
            messagebox.showinfo("Éxito", "Seguimiento_Nominal actualizado.")
            self.refrescar_lista()
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))

    def eliminar(self):
        dlg = SelectDialog(self, ["ID_SeguimientoNominal"])
        self.wait_window(dlg)
        if not getattr(dlg, "values", None):
            return
        pk = dlg.values
        confirm = ConfirmDialog(self, f"¿Eliminar Seguimiento_Nominal {pk}?")
        self.wait_window(confirm)
        if not getattr(confirm, "response", False):
            return
        try:
            self.service.eliminar(pk["ID_SeguimientoNominal"])
            messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")
            self.refrescar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))

    def _clear_form(self):
        for v in self.vars.values():
            v.set("")
