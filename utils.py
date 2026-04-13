import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    full_path = os.path.join(base_path, relative_path)

    if not os.path.exists(full_path):
        full_path = os.path.join(base_path, "logic", relative_path)

    return full_path


def obtener_ruta_recurso(carpeta, archivo):
    """
    Busca primero en la carpeta externa (pendrive/dist)
    y si no existe, usa el recurso interno del .exe.
    """
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    ruta_externa = os.path.join(base_dir, carpeta, archivo)

    if os.path.exists(ruta_externa):
        return ruta_externa

    return resource_path(os.path.join(carpeta, archivo))