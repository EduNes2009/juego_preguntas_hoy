import tkinter as tk
from tkinter import messagebox
import sys
import os
import pygame
from utils import resource_path
from config_categorias import ventana_categorias
from ui.intro_tk import run_intro

# Forzar directorio de trabajo
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
def cerrar_juego():
    try:
        pygame.mixer.stop()
        pygame.mixer.quit()
    except:
        pass
    sys.exit(0)

def iniciar_juego(root=None, reinicio=False):
    if root is None:
        root = tk.Tk()
        root.withdraw()
        root.geometry("0x0+0+0")
        
    root.protocol("WM_DELETE_WINDOW", cerrar_juego)

    # Esta función ahora recibe la "config" que envía la ventana de categorías
    def ir_a_intro(config_recibida):
        root.deiconify()

        for widget in root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                try:
                    widget.destroy()
                except:
                    pass
        run_intro(root, config_dinamica=config_recibida)

    ventana_categorias(root, callback_inicio=ir_a_intro)

    if not reinicio:
        root.mainloop()

def reiniciar_desde_main(root):
    # Limpiamos todo lo que haya en la root antes de volver a empezar
    for widget in root.winfo_children():
        widget.destroy()
    iniciar_juego(root, reinicio=True)

if __name__ == "__main__":
    iniciar_juego()