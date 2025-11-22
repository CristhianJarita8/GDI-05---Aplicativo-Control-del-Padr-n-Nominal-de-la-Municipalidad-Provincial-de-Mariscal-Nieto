import tkinter as tk
from tkinter import ttk, messagebox
from ui.dialogs.select_dialog import SelectDialog
from ui.dialogs.confirm_dialog import ConfirmDialog
from db.services.homologacion_service import HomologacionService
from ui.theme import IconButton

class HomologacionForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Homologacion_Nominal")
        self.geometry("900x520")
        self.service = HomologacionService()

        labels = [
            ("ID_HomologacionNominal",0),("FechaInicio",1),("FechaFin",2),("FechaReunion",3),
            ("Distrito",4),("Provincia",5),("Departamento",6),("Observacion",7),("NNAPS",8),("NNALM",9),
            ("NNAGIM",10),("NNDHM",11),("NNACP",12),("Nombre_EESS",13)
        ]
        self.vars = {}
        for text, idx in labels:
            ttk.Label(self, text=text).grid(row=idx, column=0, padx=6, pady=4, sticky="w")
            v = tk.StringVar()
            ttk.Entry(self, textvariable=v, width=35).grid(row=idx, column=1, padx=6, pady=4, sticky="w")
            self.vars[text] = v

        # Modificado: los botones ocupan toda la altura del formulario, no solo las primeras 8 filas.
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=0, column=2, rowspan=len(labels), padx=12, pady=6, sticky="ns")

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

        # Asegurarse que la tabla vaya después del último campo
        cols = [l[0] for l in labels]
        table_row = len(labels) + 1
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="w")
        self.tree.grid(row=table_row, column=0, columnspan=2, padx=6, pady=10, sticky="nsew")
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.grid(row=table_row, column=2, sticky="ns")

        self.grid_rowconfigure(table_row, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.refrescar_lista()

    def _read_form(self):
        return (
            self.vars["ID_HomologacionNominal"].get().strip(),
            self.vars["FechaInicio"].get().strip(),
            self.vars["FechaFin"].get().strip(),
            self.vars["FechaReunion"].get().strip(),
            self.vars["Distrito"].get().strip(),
            self.vars["Provincia"].get().strip(),
            self.vars["Departamento"].get().strip(),
            self.vars["Observacion"].get().strip(),
            self.vars["NNAPS"].get().strip(),
            self.vars["NNALM"].get().strip(),
            self.vars["NNAGIM"].get().strip(),
            self.vars["NNDHM"].get().strip(),
            self.vars["NNACP"].get().strip(),
            self.vars["Nombre_EESS"].get().strip()
        )

    def insertar(self):
        data = self._read_form()
        if not all(data):
            messagebox.showwarning("Validación", "Complete todos los campos antes de insertar.")
            return
        try:
            self.service.crear(data)
            messagebox.showinfo("Éxito", "Homologacion_Nominal insertada.")
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
        dlg = SelectDialog(self, ["ID_HomologacionNominal"])
        self.wait_window(dlg)
        if not getattr(dlg, "values", None):
            return
        pk = dlg.values
        try:
            row = self.service.get_by_pk(pk["ID_HomologacionNominal"])
            if not row:
                messagebox.showinfo("No encontrado", "No hay registro con esas claves.")
                return
            for key in self.vars:
                if "Fecha" in key and getattr(row.get(key), "strftime", None):
                    self.vars[key].set((row.get(key) or "").strftime("%Y-%m-%d"))
                else:
                    self.vars[key].set(row.get(key) or "")
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))

    def actualizar(self):
        data = self._read_form()
        if not (data[0]):
            messagebox.showwarning("PK faltante", "ID_HomologacionNominal es obligatorio para actualizar.")
            return
        try:
            self.service.modificar(data)
            messagebox.showinfo("Éxito", "Homologacion_Nominal actualizada.")
            self.refrescar_lista()
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))

    def eliminar(self):
        dlg = SelectDialog(self, ["ID_HomologacionNominal"])
        self.wait_window(dlg)
        if not getattr(dlg, "values", None):
            return
        pk = dlg.values
        confirm = ConfirmDialog(self, f"¿Eliminar Homologacion_Nominal {pk}?")
        self.wait_window(confirm)
        if not getattr(confirm, "response", False):
            return
        try:
            self.service.eliminar(pk["ID_HomologacionNominal"])
            messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")
            self.refrescar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))

    def _clear_form(self):
        for v in self.vars.values():
            v.set("")
