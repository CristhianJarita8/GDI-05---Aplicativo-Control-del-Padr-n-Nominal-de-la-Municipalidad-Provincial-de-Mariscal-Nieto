import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import mysql.connector
from mysql.connector import Error

class DBConnection:
    def __init__(self, host: str = "localhost", user: str = "root", password: str = "", database: str = "nominal_db", port: int = 3306):
        self.config = {"host": host, "user": user, "password": password, "database": database, "port": port}
        self.conn: Optional[mysql.connector.connection.MySQLConnection] = None

    def open(self):
        if self.conn and self.conn.is_connected():
            return
        self.conn = mysql.connector.connect(**self.config)

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            self.conn = None


@dataclass
class PadronNominal:
    Codigo_PadronNominal: str
    Numero_DNI: str
    EstadoTramite_DNI: Optional[str] = None
    FechaTramite_DNI: Optional[str] = None
    Tipo_Docuemtno: Optional[str] = None
    CodigoUnico_Identidad: Optional[str] = None
    Numero_CertificadoNacidoVido: Optional[str] = None
    Direccion: Optional[str] = None
    Telefono: Optional[str] = None
    Historial_Clinico: Optional[str] = None
    DNI_CE: Optional[str] = None


class PadronRepository(ABC):
    @abstractmethod
    def insert(self, padron: PadronNominal) -> None: ...
    @abstractmethod
    def update(self, codigo: str, updates: Dict[str, Any]) -> None: ...
    @abstractmethod
    def fetch_all(self) -> List[Dict[str, Any]]: ...
    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[Dict[str, Any]]: ...

class MySQLPadronRepository(PadronRepository):
    def __init__(self, db: DBConnection):
        self.db = db

    def insert(self, padron: PadronNominal) -> None:
        sql = """
        INSERT INTO Padron_Nominal
        (Codigo_PadronNominal, Numero_DNI, EstadoTramite_DNI, FechaTramite_DNI,
         Tipo_Docuemtno, CodigoUnico_Identidad, Numero_CertificadoNacidoVido,
         Direccion, Telefono, Historial_Clinico, DNI_CE)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        vals = (
            padron.Codigo_PadronNominal, padron.Numero_DNI, padron.EstadoTramite_DNI,
            padron.FechaTramite_DNI, padron.Tipo_Docuemtno, padron.CodigoUnico_Identidad,
            padron.Numero_CertificadoNacidoVido, padron.Direccion, padron.Telefono,
            padron.Historial_Clinico, padron.DNI_CE
        )
        cur = None
        try:
            self.db.open()
            cur = self.db.conn.cursor()
            cur.execute(sql, vals)
            self.db.conn.commit()
        except Error:
            if self.db.conn and self.db.conn.is_connected():
                self.db.conn.rollback()
            raise
        finally:
            if cur is not None:
                cur.close()

    def update(self, codigo: str, updates: Dict[str, Any]) -> None:
        if not updates:
            return
        keys = list(updates.keys())
        set_clause = ", ".join(f"{k} = %s" for k in keys)
        sql = f"UPDATE Padron_Nominal SET {set_clause} WHERE Codigo_PadronNominal = %s"
        vals = tuple(updates[k] for k in keys) + (codigo,)
        cur = None
        try:
            self.db.open()
            cur = self.db.conn.cursor()
            cur.execute(sql, vals)
            self.db.conn.commit()
        except Error:
            if self.db.conn and self.db.conn.is_connected():
                self.db.conn.rollback()
            raise
        finally:
            if cur is not None:
                cur.close()

    def fetch_all(self) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM Padron_Nominal"
        cur = None
        try:
            self.db.open()
            cur = self.db.conn.cursor(dictionary=True)
            cur.execute(sql)
            rows = cur.fetchall()
            return rows
        finally:
            if cur is not None:
                cur.close()

    def get_by_codigo(self, codigo: str) -> Optional[Dict[str, Any]]:
        sql = "SELECT * FROM Padron_Nominal WHERE Codigo_PadronNominal = %s"
        cur = None
        try:
            self.db.open()
            cur = self.db.conn.cursor(dictionary=True)
            cur.execute(sql, (codigo,))
            row = cur.fetchone()
            return row
        finally:
            if cur is not None:
                cur.close()


class PadronService:
    def __init__(self, repo: PadronRepository):
        self.repo = repo

    def create_padron(self, padron: PadronNominal):
        if not padron.Codigo_PadronNominal or not padron.Numero_DNI:
            raise ValueError("Codigo_PadronNominal y Numero_DNI son obligatorios")
        self.repo.insert(padron)

    def modify_padron(self, codigo: str, updates: Dict[str, Any]):
        if not codigo:
            raise ValueError("Codigo requerido")
        self.repo.update(codigo, updates)

    def list_padron(self) -> List[Dict[str, Any]]:
        return self.repo.fetch_all()

    def get_padron(self, codigo: str) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_codigo(codigo)


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Gestión Padron Nominal")

        # Configuración automática de conexión
        self.db = DBConnection(
            host="localhost",
            user="root",
            password="root",  
            database="nominal_db"
        )

        try:
            self.db.open()
            self.repo = MySQLPadronRepository(self.db)
            self.service = PadronService(self.repo)
            messagebox.showinfo("Conexión", "Conectado automáticamente a la base de datos")
        except Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar: {e}")
            self.repo = None
            self.service = None

        self._build_action_frame()

    def _build_action_frame(self):
        frm = ttk.Frame(self.root)
        frm.pack(fill="x", padx=8, pady=6)

        self.insert_btn = ttk.Button(frm, text="Insertar registro", command=self.open_insert_window)
        self.insert_btn.grid(row=0, column=0, padx=6, pady=4)

        self.view_btn = ttk.Button(frm, text="Ver registros", command=self.open_view_window)
        self.view_btn.grid(row=0, column=1, padx=6, pady=4)

        self.update_btn = ttk.Button(frm, text="Modificar registro", command=self.open_update_window)
        self.update_btn.grid(row=0, column=2, padx=6, pady=4)

    def open_insert_window(self):
        win = tk.Toplevel(self.root)
        win.title("Insertar Padron")
        fields = ["Codigo_PadronNominal", "Numero_DNI", "EstadoTramite_DNI", "FechaTramite_DNI", "Tipo_Docuemtno",
                  "CodigoUnico_Identidad", "Numero_CertificadoNacidoVido", "Direccion", "Telefono", "Historial_Clinico", "DNI_CE"]
        vars = {f: tk.StringVar() for f in fields}

        for i, f in enumerate(fields):
            ttk.Label(win, text=f).grid(row=i, column=0, sticky="w", padx=6, pady=3)
            ttk.Entry(win, textvariable=vars[f], width=40).grid(row=i, column=1, padx=6, pady=3)

        def submit():
            try:
                padron = PadronNominal(**{k: (v.get().strip() or None) for k, v in vars.items()})
                if self.service is None:
                    raise RuntimeError("Servicio no inicializado")
                self.service.create_padron(padron)
                messagebox.showinfo("Éxito", "Registro insertado correctamente")
                win.destroy()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(win, text="Guardar", command=submit).grid(row=len(fields), column=0, columnspan=2, pady=8)

    def open_view_window(self):
        win = tk.Toplevel(self.root)
        win.title("Registros Padron_Nominal")
        cols = ["Codigo_PadronNominal", "Numero_DNI", "EstadoTramite_DNI", "FechaTramite_DNI", "Tipo_Docuemtno",
                "CodigoUnico_Identidad", "Numero_CertificadoNacidoVido", "Direccion", "Telefono", "Historial_Clinico", "DNI_CE"]
        tree = ttk.Treeview(win, columns=cols, show="headings", height=15)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor="w")
        tree.pack(fill="both", expand=True, padx=6, pady=6)

        scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        try:
            if self.service is None:
                raise RuntimeError("Servicio no inicializado")
            rows = self.service.list_padron()
            for r in rows:
                values = [r.get(c) for c in cols]
                tree.insert("", "end", values=values)
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def open_update_window(self):
        win = tk.Toplevel(self.root)
        win.title("Modificar Padron")
        ttk.Label(win, text="Codigo_PadronNominal").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        codigo_var = tk.StringVar()
        ttk.Entry(win, textvariable=codigo_var, width=30).grid(row=0, column=1, padx=6, pady=6)

        fields = ["Numero_DNI", "EstadoTramite_DNI", "FechaTramite_DNI", "Tipo_Docuemtno",
                  "CodigoUnico_Identidad", "Numero_CertificadoNacidoVido", "Direccion", "Telefono", "Historial_Clinico", "DNI_CE"]
        vars = {f: tk.StringVar() for f in fields}

        for i, f in enumerate(fields, start=1):
            ttk.Label(win, text=f).grid(row=i, column=0, sticky="w", padx=6, pady=3)
            ttk.Entry(win, textvariable=vars[f], width=40).grid(row=i, column=1, padx=6, pady=3)

        def load():
            codigo = codigo_var.get().strip()
            if not codigo:
                messagebox.showwarning("Validación", "Ingrese Codigo_PadronNominal")
                return
            try:
                if self.service is None:
                    raise RuntimeError("Servicio no inicializado")
                row = self.service.get_padron(codigo)
                if not row:
                    messagebox.showinfo("No encontrado", "No existe un registro con ese código")
                    return
                for f in fields:
                    vars[f].set(row.get(f) or "")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        def submit_update():
            codigo = codigo_var.get().strip()
            updates = {f: vars[f].get().strip() for f in fields if vars[f].get().strip()}
            if not updates:
                messagebox.showinfo("Sin cambios", "No hay campos para actualizar")
                return
            try:
                if self.service is None:
                    raise RuntimeError("Servicio no inicializado")
                self.service.modify_padron(codigo, updates)
                messagebox.showinfo("Éxito", "Registro actualizado correctamente")
                win.destroy()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(win, text="Cargar", command=load).grid(row=0, column=2, padx=6, pady=6)
        ttk.Button(win, text="Actualizar", command=submit_update).grid(row=len(fields) + 1, column=0, columnspan=3, pady=8)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    if app.db:
        app.db.close()

if __name__ == "__main__":
    main()
