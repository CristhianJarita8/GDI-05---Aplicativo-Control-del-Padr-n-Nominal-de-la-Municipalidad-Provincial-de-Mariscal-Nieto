import tkinter as tk
from ui.theme import init_theme
from ui.main_window import MainMenu

if __name__ == "__main__":
    root = MainMenu()
    init_theme(root)
    root.mainloop()
