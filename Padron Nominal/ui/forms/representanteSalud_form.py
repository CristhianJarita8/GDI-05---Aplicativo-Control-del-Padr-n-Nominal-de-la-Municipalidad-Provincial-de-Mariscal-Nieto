import tkinter as tk
from tkinter import ttk, messagebox
from ui.dialogs.select_dialog import SelectDialog
from ui.dialogs.confirm_dialog import ConfirmDialog
from db.services.representanteSalud_service import RepresentanteSaludService
from ui.theme import IconButton

class RepresentanteSaludForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Representante_Salud")
        self.geometry("900x520")
        self.service = RepresentanteSaludService()

        labels = [("DNI_RS",0),("ID_HomologacionNominal",1),("Nombre_RS",2)]
        self.vars = {}
        for text, idx in labels:
            ttk.Label(self, text=text).grid(row=idx, column=0, padx=6, pady=4, sticky="w")
            v = tk.StringVar()
            ttk.Entry(self, textvariable=v, width=40).grid(row=idx, column=1, padx=6, pady=4, sticky="w")
            self.vars[text] = v

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=0, column=3, rowspan=4, padx=12, pady=6, sticky="n")

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


        cols = ["DNI_RS","ID_HomologacionNominal","Nombre_RS"]
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
            self.vars["DNI_RS"].get().strip(),
            self.vars["ID_HomologacionNominal"].get().strip(),
            self.vars["Nombre_RS"].get().strip()
        )

    def insertar(self):
        data = self._read_form()
        if not all(data):
            messagebox.showwarning("Validación", "Complete todos los campos antes de insertar.")
            return
        try:
            self.service.crear(data)
            messagebox.showinfo("Éxito", "Representante_Salud insertado.")
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
        dlg = SelectDialog(self, ["DNI_RS","ID_HomologacionNominal"])
        self.wait_window(dlg)
        if not getattr(dlg, "values", None):
            return
        pk = dlg.values
        try:
            row = self.service.get_by_pk(pk["DNI_RS"], pk["ID_HomologacionNominal"])
            if not row:
                messagebox.showinfo("No encontrado", "No hay registro con esas claves.")
                return
            self.vars["DNI_RS"].set(row.get("DNI_RS") or "")
            self.vars["ID_HomologacionNominal"].set(row.get("ID_HomologacionNominal") or "")
            self.vars["Nombre_RS"].set(row.get("Nombre_RS") or "")
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))

    def actualizar(self):
        data = self._read_form()
        if not (data[0] and data[1]):
            messagebox.showwarning("PK faltante", "DNI_RS y ID_HomologacionNominal son obligatorios para actualizar.")
            return
        try:
            self.service.modificar(data)
            messagebox.showinfo("Éxito", "Representante_Salud actualizado.")
            self.refrescar_lista()
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))

    def eliminar(self):
        dlg = SelectDialog(self, ["DNI_RS","ID_HomologacionNominal"])
        self.wait_window(dlg)
        if not getattr(dlg, "values", None):
            return
        pk = dlg.values
        confirm = ConfirmDialog(self, f"¿Eliminar Representante_Salud {pk}?")
        self.wait_window(confirm)
        if not getattr(confirm, "response", False):
            return
        try:
            self.service.eliminar(pk["DNI_RS"], pk["ID_HomologacionNominal"])
            messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")
            self.refrescar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))

    def _clear_form(self):
        for v in self.vars.values():
            v.set("")
