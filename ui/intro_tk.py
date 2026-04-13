import tkinter as tk
import pygame
import os

from ui.efecto_matrix import EfectoMatrix
from ui.styles import BACKGROUND_COLOR
from utils import resource_path
from efectos_texto import crear_texto_verde_metalico, crear_texto_verde_metalico_titulo
from ui.players_window import PlayersWindow

# ================== INTRO ==================
anim_id_global = None

def run_intro(root, config_dinamica=None):

    try:
        pygame.mixer.music.stop()
    except:
        pass

    pygame.mixer.init()
    pygame.mixer.music.load(resource_path("sounds/intro.mp3"))
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)

    ventana_intro = tk.Toplevel(root)
    ventana_intro.attributes("-fullscreen", True)
    ventana_intro.configure(bg=BACKGROUND_COLOR)

    ventana_intro.update_idletasks()
    width = ventana_intro.winfo_width()
    height = ventana_intro.winfo_height()

    efecto_matrix = EfectoMatrix(ventana_intro, width, height)

    alto = ventana_intro.winfo_height()
    size = max(20, alto // 15)
    offsets = [(-2,0), (2,0), (0,-2), (0,2), (-2,-2), (-2,2), (2,-2), (2,2)]

    for dx, dy in offsets:
        efecto_matrix.canvas.create_text(
            width//2 + dx, height//2 + dy,
            text="BIENVENIDOS AL JUEGO",
            fill="black",
            font=("Consolas", size, "bold"),
            anchor="center"
        )

    efecto_matrix.canvas.create_text(
        width//2, height//2,
        text="BIENVENIDOS AL JUEGO",
        fill="#00FF9c",
        font=("Consolas", size, "bold"),
        anchor="center"
    )

    def cerrar_intro():
        global anim_id_global
        try:
            pygame.mixer.music.stop()
        except:
            pass
        # Aquí deberías cancelar la animación de Matrix si guardaste el ID
        ventana_intro.destroy()

    # 2. Modificamos esta función para que pase la config a la siguiente ventana
    def pasar_a_jugadores():
        cerrar_intro()
        # Le pasamos la config a PlayersWindow
        # (Asegúrate de que PlayersWindow acepte este argumento en su __init__)
        PlayersWindow(root, config_dinamica=config_dinamica) 

    # El juego pasa solo a los 5 segundos
    ventana_intro.after(5000, pasar_a_jugadores)

    ventana_intro.bind("<Escape>", lambda e: cerrar_intro())
    ventana_intro.protocol("WM_DELETE_WINDOW", cerrar_intro)

    ventana_intro.focus_force()
    ventana_intro.grab_set()
    return ventana_intro