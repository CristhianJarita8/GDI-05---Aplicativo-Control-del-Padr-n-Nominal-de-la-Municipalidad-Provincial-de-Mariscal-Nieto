import tkinter as tk
from tkinter import ttk

from ui.theme import init_theme, IconButton

from ui.forms.padron_form import PadronForm
from ui.forms.infante_form import InfanteForm
from ui.forms.visita_form import FichaVisitaForm
from ui.forms.apoderado_form import ApoderadoForm
from ui.forms.homologacion_form import HomologacionForm
from ui.forms.seguimiento_form import SeguimientoForm
from ui.forms.informacion_form import InformacionInfanteForm
from ui.forms.representanteSalud_form import RepresentanteSaludForm
from ui.forms.representanteMunicipal_form import RepresentanteMunicipalForm
from ui.forms.reportes_form import ReportesForm


class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        # Inicializar theme
        init_theme(self)

        self.title("Sistema Padrón Nominal")
        self.geometry("400x600")
        self.resizable(False, False)

        # ===============================
        # HEADER
        # ===============================

        header = ttk.Label(
            self,
            text="GESTIÓN NOMINAL",
            style="Header.TLabel",
            anchor="center"
        )
        header.pack(pady=20)

        # ===============================
        # CARD (contenedor principal)
        # ===============================

        card = ttk.Frame(self, style="Card.TFrame", padding=15)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        # ===============================
        # Lista de opciones con iconos
        # ===============================

        opciones = [
            ("Padrón Nominal", "padron", PadronForm),
            ("Infantes", "infante", InfanteForm),
            ("Fichas de Visita", "visita", FichaVisitaForm),
            ("Apoderados", "apoderado", ApoderadoForm),
            ("Homologaciones", "homologacion", HomologacionForm),
            ("Seguimientos", "seguimiento", SeguimientoForm),
            ("Información del Infante", "informacion", InformacionInfanteForm),
            ("Representantes Salud", "salud", RepresentanteSaludForm),
            ("Representantes Municipales", "municipal", RepresentanteMunicipalForm),
            ("Reportes", "report", ReportesForm),
        ]

        # ===============================
        # Botones con IconButton
        # ===============================

        for texto, icono, formulario in opciones:
            boton = IconButton(
                card,
                icon_name=icono,
                text=texto,
                command=lambda f=formulario: f(self),
                icon_size=20
            )
            boton.pack(fill="x", pady=6)

        # Espaciador limpio (sin usar background inválido)
        ttk.Label(card, text="").pack(pady=5)


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
