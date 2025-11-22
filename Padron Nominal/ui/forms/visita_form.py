import tkinter as tk
from tkinter import ttk, messagebox
from ui.dialogs.select_dialog import SelectDialog
from ui.dialogs.confirm_dialog import ConfirmDialog
from db.services.visita_service import FichaVisitaService
from ui.theme import IconButton

class FichaVisitaForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ficha_Visita")
        self.geometry("900x520")
        self.service = FichaVisitaService()

        labels = [
            ("DNI_CE",0),("Codigo_PadronNominal",1),("Fecha_Visita",2),("Peso_Infante",3),
            ("Distrito",4),("Fecha_Nacimiento",5),("LenguaMaterna",6),("ID_HomologacionNominal",7)
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
        ).grid


        cols = ["ID_Visita","DNI_CE","Codigo_PadronNominal","Fecha_Visita","Peso_Infante","Distrito","Fecha_Nacimiento","LenguaMaterna","ID_HomologacionNominal"]
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
            self.vars["Fecha_Visita"].get().strip(),
            self.vars["Peso_Infante"].get().strip(),
            self.vars["Distrito"].get().strip(),
            self.vars["Fecha_Nacimiento"].get().strip(),
            self.vars["LenguaMaterna"].get().strip(),
            self.vars["ID_HomologacionNominal"].get().strip()
        )

    def insertar(self):
        data = self._read_form()
        if not all(data):
            messagebox.showwarning("Validación", "Complete todos los campos antes de insertar.")
            return
        try:
            self.service.crear(data)
            messagebox.showinfo("Éxito", "Ficha_Visita insertada.")
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
        dlg = SelectDialog(self, ["ID_Visita"])
        self.wait_window(dlg)
        if not getattr(dlg, "values", None):
            return
        pk = dlg.values
        try:
            row = self.service.get_by_pk(int(pk["ID_Visita"]))
            if not row:
                messagebox.showinfo("No encontrado", "No hay registro con esas claves.")
                return
            self.vars["DNI_CE"].set(row.get("DNI_CE") or "")
            self.vars["Codigo_PadronNominal"].set(row.get("Codigo_PadronNominal") or "")
            self.vars["Fecha_Visita"].set((row.get("Fecha_Visita") or "").strftime("%Y-%m-%d") if getattr(row.get("Fecha_Visita"), "strftime", None) else (row.get("Fecha_Visita") or ""))
            self.vars["Peso_Infante"].set(str(row.get("Peso_Infante") or ""))
            self.vars["Distrito"].set(row.get("Distrito") or "")
            self.vars["Fecha_Nacimiento"].set((row.get("Fecha_Nacimiento") or "").strftime("%Y-%m-%d") if getattr(row.get("Fecha_Nacimiento"), "strftime", None) else (row.get("Fecha_Nacimiento") or ""))
            self.vars["LenguaMaterna"].set(row.get("LenguaMaterna") or "")
            self.vars["ID_HomologacionNominal"].set(row.get("ID_HomologacionNominal") or "")
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))

    def actualizar(self):
        data = self._read_form()
        # note: identification for update is ID_Visita; user should load it first
        if not data[0] and not data[1]:
            messagebox.showwarning("PK faltante", "Debe indicar al menos DNI_CE y Codigo_PadronNominal o usar cargar para obtener ID.")
            return
        try:
            self.service.modificar(data)
            messagebox.showinfo("Éxito", "Ficha_Visita actualizada.")
            self.refrescar_lista()
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))

    def eliminar(self):
        dlg = SelectDialog(self, ["ID_Visita"])
        self.wait_window(dlg)
        if not getattr(dlg, "values", None):
            return
        pk = dlg.values
        confirm = ConfirmDialog(self, f"¿Eliminar Ficha_Visita {pk}?")
        self.wait_window(confirm)
        if not getattr(confirm, "response", False):
            return
        try:
            self.service.eliminar(int(pk["ID_Visita"]))
            messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")
            self.refrescar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))

    def _clear_form(self):
        for v in self.vars.values():
            v.set("")
