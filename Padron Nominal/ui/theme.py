import os
import tkinter as tk
from tkinter import ttk, PhotoImage

# ===============================================================
# PALETTE
# ===============================================================

PALETTE = {
    "bg": "#326599",  # fondo general
    "fg": "#1A1A1A",  # texto oscuro
    "primary": "#005BBB",  # azul primario
    "primary_hover": "#0077EE",  # azul hover
    "danger": "#D32F2F",  # color de error
    "card": "#FFFFFF",  # fondo tarjetas
    "border": "#DDDDDD",  # borde claro
    "button_bg": "#EEEEEE",  # color de fondo de los botones
    "button_hover": "#E0E0E0",  # hover en botones
}

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# ===============================================================
# ICON LOADER (NECESARIO PARA TUS FORMS ACTUALES)
# ===============================================================

def load_icon(name, size=24):
    """Cargar un icono PNG desde /assets"""
    path = os.path.join(ASSETS_DIR, f"{name}.png")

    # Si existe el archivo
    if os.path.exists(path):
        try:
            img = PhotoImage(file=path)
            scale = max(1, img.width() // size)
            return img.subsample(scale)
        except Exception:
            pass

    # fallback cuadrado azul si no existe
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

    # ============================
    # Estilo de las frames
    # ============================
    style.configure("Main.TFrame", background=PALETTE["bg"])  # fondo ventana principal
    style.configure("Card.TFrame", background=PALETTE["card"])  # fondo de las tarjetas

    # ============================
    # Estilo de las etiquetas
    # ============================
    style.configure(
        "Title.TLabel",
        font=("Segoe UI", 14, "bold"),
        foreground=PALETTE["fg"],
    )

    # ============================
    # Estilo de los botones
    # ============================
    style.configure(
        "TButton",
        foreground=PALETTE["fg"],
        borderwidth=1,
        padding=8,
    )
    style.map(
        "TButton",
        background=[("active", PALETTE["button_hover"])]  # color al pasar el cursor
    )

    # ============================
    # Botones del menú (con icono)
    # ============================
    style.configure(
        "MenuButton.TButton",
        background=PALETTE["card"],
        foreground=PALETTE["fg"],
        font=("Segoe UI", 11, "bold"),
        padding=10,
        relief="flat",
    )
    style.map(
        "MenuButton.TButton",
        background=[("hover", PALETTE["button_hover"]), ("active", PALETTE["primary"])],
        foreground=[("active", "#FFFFFF")],
    )

    # ============================
    # Botones con icono + texto
    # ============================
    style.configure(
        "Line.TButton",
        background=PALETTE["card"],
        foreground=PALETTE["fg"],
        padding=6,
        borderwidth=0,
    )
    style.map(
        "Line.TButton",
        background=[("hover", PALETTE["button_hover"]), ("active", PALETTE["primary"])],
        foreground=[("active", "#FFFFFF")],
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
