import os
import tkinter as tk
from tkinter import ttk, PhotoImage

# ===============================================================
# PALETTE
# ===============================================================

PALETTE = {
    "bg": "#5794BD",           # Fondo general
    "fg": "#ffffff",           # Texto general/blanco
    "primary": "#368AE4",      # Azul primario
    "primary_hover": "#0077EE",# Azul hover
    "danger": "#D32F2F",       # Color de error/advertencia
    "header": "#173F5F",       # Fondo header
    "card": "#2c3454",         # Fondo tarjetas/contenedores
    "border": "#2e477e",       # Borde claro
    "button_bg": "#1768AC",    # Fondo de los botones
    "button_hover": "#F0A2A2", # Hover de los botones
    "button_border": "#1C93CE", # nuevo color para el borde de los botones
    "entry_bg": "#FFFFFF",     # Fondo de entradas de texto
    "entry_fg": "#1A1A1A",     # Texto en las entradas
    "tree_heading_bg": "#368AE4", # Fondo cabecera tablas
    "tree_heading_fg": "#ffffff", # Texto cabecera tablas
    "tree_bg": "#ecb3a2",         # Fondo filas de la tabla
    "tree_fg": "#000000",         # Texto filas de la tabla
    "tree_selected_bg": "#4CB0F9",# Fondo fila seleccionada
    "tree_selected_fg": "#173F5F" # Texto fila seleccionada
}

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# ===============================================================
# ICON LOADER (NECESARIO PARA TUS FORMS ACTUALES)
# ===============================================================

def load_icon(name, size=24):
    path = os.path.join(ASSETS_DIR, f"{name}.png")
    if os.path.exists(path):
        try:
            img = PhotoImage(file=path)
            scale = max(1, img.width() // size)
            return img.subsample(scale)
        except Exception:
            pass
    img = PhotoImage(width=size, height=size)
    for y in range(size):
        img.put(PALETTE["primary"], to=(0, y, size, y+1))
    return img

# ===============================================================
# THEME (estilos generales)
# ===============================================================

def init_theme(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    # Estilo de frames principales y cards
    style.configure("Main.TFrame", background=PALETTE["bg"])
    style.configure("Card.TFrame", background=PALETTE["card"])

    # Header grande
    style.configure(
        "Header.TLabel",
        font=("Segoe UI", 18, "bold"),
        foreground=PALETTE["fg"],
        background=PALETTE["header"],
        anchor="center"
    )

    # Subtitulo o secciones
    style.configure(
        "Title.TLabel",
        font=("Segoe UI", 14, "bold"),
        foreground=PALETTE["primary"],
        background=PALETTE["card"]
    )

    # Estilo de botones
    style.configure(
        "TButton",
        background=PALETTE["button_bg"],
        foreground=PALETTE["fg"],
        borderwidth=2,                 # más ancho para que se note el color
        relief="solid",                # borde sólido visible
        bordercolor=PALETTE["button_border"],
        padding=8
    )
    style.map(
        "TButton",
        background=[("active", PALETTE["button_hover"])],
        foreground=[("active", "#FFFFFF")]
    )

    # Botones con icono menú
    style.configure(
        "MenuButton.TButton",
        background=PALETTE["card"],
        foreground=PALETTE["fg"],
        font=("Segoe UI", 11, "bold"),
        padding=10,
        relief="solid",     # antes: flat
        borderwidth=2,
        bordercolor=PALETTE["button_border"],
    )
    style.map("MenuButton.TButton",
        background=[("hover", PALETTE["button_hover"]), ("active", PALETTE["primary"])],
        foreground=[("active", "#FFFFFF")]
    )

    # Botones con icono + texto (los usados en tus formularios)
    style.configure(
        "Line.TButton",
        background=PALETTE["card"],
        foreground=PALETTE["fg"],
        padding=6,
        borderwidth=2,
        bordercolor=PALETTE["button_border"],
        relief="solid"
    )
    style.map("Line.TButton",
        background=[("hover", PALETTE["button_hover"]), ("active", PALETTE["primary"])],
        foreground=[("active", "#FFFFFF")]
    )

    # Entradas de texto
    style.configure(
        "TEntry",
        foreground=PALETTE["entry_fg"],
        fieldbackground=PALETTE["entry_bg"],
        background=PALETTE["entry_bg"]
    )

    # Scrollbar
    style.configure("Vertical.TScrollbar", background=PALETTE["primary"])
    style.configure("Horizontal.TScrollbar", background=PALETTE["primary"])

    # Treeview (tablas)
    style.configure(
        "Treeview",
        background=PALETTE["tree_bg"],
        foreground=PALETTE["tree_fg"],
        fieldbackground=PALETTE["tree_bg"],
        bordercolor=PALETTE["border"]
    )
    style.map(
        "Treeview",
        background=[("selected", PALETTE["tree_selected_bg"])],
        foreground=[("selected", PALETTE["tree_selected_fg"])]
    )
    style.configure(
        "Treeview.Heading",
        background=PALETTE["tree_heading_bg"],
        foreground=PALETTE["tree_heading_fg"],
        font=("Segoe UI", 11, "bold")
    )

# ===============================================================
# ICON BUTTON CLASS (COMPATIBLE)
# ===============================================================

class IconButton(ttk.Frame):
    def __init__(self, parent, icon_name, text="", command=None, icon_size=24):
        super().__init__(parent, style="Card.TFrame")
        self.command = command
        self.icon_img = load_icon(icon_name, icon_size)

        self.button = ttk.Button(
            self,
            image=self.icon_img,
            text=text,
            compound="left",
            command=self._run_cmd,
            style="Line.TButton"
        )
        self.button.pack(fill="x", expand=True)

    def _run_cmd(self):
        if self.command:
            self.command()