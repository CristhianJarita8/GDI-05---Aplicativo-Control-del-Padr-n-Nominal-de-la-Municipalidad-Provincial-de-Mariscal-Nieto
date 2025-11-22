import tkinter as tk
from tkinter import ttk, messagebox
from ui.dialogs.select_dialog import SelectDialog
from ui.dialogs.confirm_dialog import ConfirmDialog
from db.services.padron_service import PadronNominalService
from ui.theme import IconButton

class PadronForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Padron_Nominal")
        self.geometry("900x700")
        self.service = PadronNominalService()

        labels = [
            ("Codigo_PadronNominal",0),("Numero_DNI",1),("EstadoTramite_DNI",2),("FechaTramite_DNI",3),
            ("Tipo_Documento",4),("CodigoUnico_Identidad",5),("Numero_CertificadoNacidoVivo",6),
            ("Direccion",7),("Telefono",8),("Historial_Clinico",9),("DNI_CE",10)
        ]
        self.vars = {}
        
        for text, idx in labels:
            ttk.Label(self, text=text).grid(row=idx, column=0, padx=6, pady=4, sticky="w")
            v = tk.StringVar()
            ttk.Entry(self, textvariable=v, width=35).grid(row=idx, column=1, padx=6, pady=4, sticky="w")
            self.vars[text] = v

        # Coloca el frame de botones a la derecha, ocupando toda la altura de los campos
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


        cols = ["Codigo_PadronNominal","Numero_DNI","EstadoTramite_DNI","FechaTramite_DNI","Tipo_Documento",
                "CodigoUnico_Identidad","Numero_CertificadoNacidoVivo","Direccion","Telefono","Historial_Clinico","DNI_CE"]
        
        table_row = len(labels) + 1

        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="w")
        self.tree.grid(row=table_row, column=0, columnspan=3, padx=6, pady=10, sticky="nsew")

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.grid(row=table_row, column=3, sticky="ns")

        # Expande columna 1 (entradas) y fila de la tabla
        self.grid_rowconfigure(table_row, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.refrescar_lista()

    def _read_form(self):
        return (
            self.vars["Codigo_PadronNominal"].get().strip(),
            self.vars["Numero_DNI"].get().strip(),
            self.vars["EstadoTramite_DNI"].get().strip(),
            self.vars["FechaTramite_DNI"].get().strip(),
            self.vars["Tipo_Documento"].get().strip(),
            self.vars["CodigoUnico_Identidad"].get().strip(),
            self.vars["Numero_CertificadoNacidoVivo"].get().strip(),
            self.vars["Direccion"].get().strip(),
            self.vars["Telefono"].get().strip(),
            self.vars["Historial_Clinico"].get().strip(),
            self.vars["DNI_CE"].get().strip()
        )

    def insertar(self):
        data = self._read_form()
        if not all(data):
            messagebox.showwarning("Validación", "Complete todos los campos antes de insertar.")
            return
        try:
            self.service.crear(data)
            messagebox.showinfo("Éxito", "Padron_Nominal insertado.")
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
        dlg = SelectDialog(self, ["Codigo_PadronNominal"])
        self.wait_window(dlg)
        if not getattr(dlg, "values", None):
            return
        pk = dlg.values
        try:
            row = self.service.get_by_pk(pk["Codigo_PadronNominal"])
            if not row:
                messagebox.showinfo("No encontrado", "No hay registro con esas claves.")
                return
            self.vars["Codigo_PadronNominal"].set(row.get("Codigo_PadronNominal") or "")
            self.vars["Numero_DNI"].set(row.get("Numero_DNI") or "")
            self.vars["EstadoTramite_DNI"].set(row.get("EstadoTramite_DNI") or "")
            self.vars["FechaTramite_DNI"].set((row.get("FechaTramite_DNI") or "").strftime("%Y-%m-%d") if getattr(row.get("FechaTramite_DNI"), "strftime", None) else (row.get("FechaTramite_DNI") or ""))
            self.vars["Tipo_Documento"].set(row.get("Tipo_Documento") or "")
            self.vars["CodigoUnico_Identidad"].set(row.get("CodigoUnico_Identidad") or "")
            self.vars["Numero_CertificadoNacidoVivo"].set(row.get("Numero_CertificadoNacidoVivo") or "")
            self.vars["Direccion"].set(row.get("Direccion") or "")
            self.vars["Telefono"].set(row.get("Telefono") or "")
            self.vars["Historial_Clinico"].set(row.get("Historial_Clinico") or "")
            self.vars["DNI_CE"].set(row.get("DNI_CE") or "")
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))

    def actualizar(self):
        data = self._read_form()
        if not (data[0]):
            messagebox.showwarning("PK faltante", "Codigo_PadronNominal es obligatorio para actualizar.")
            return
        try:
            self.service.modificar(data)
            messagebox.showinfo("Éxito", "Padron_Nominal actualizado.")
            self.refrescar_lista()
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))

    def eliminar(self):
        dlg = SelectDialog(self, ["Codigo_PadronNominal"])
        self.wait_window(dlg)
        if not getattr(dlg, "values", None):
            return
        pk = dlg.values
        confirm = ConfirmDialog(self, f"¿Eliminar Padron_Nominal {pk}?")
        self.wait_window(confirm)
        if not getattr(confirm, "response", False):
            return
        try:
            self.service.eliminar(pk["Codigo_PadronNominal"])
            messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")
            self.refrescar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))

    def _clear_form(self):
        for v in self.vars.values():
            v.set("")
