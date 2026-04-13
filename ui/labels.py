import tkinter as tk
from ui.styles import BG_MAIN, BG_PANEL
import textwrap
import os
from PIL import ImageFont, Image, ImageTk
from utils import resource_path
from efectos_texto import (
    crear_texto_dorado,
    crear_texto_dorado_con_copas,
    crear_texto_verde_metalico, crear_texto_verde_metalico_pack
)
from ui.buttons import crear_boton_redondeado


# =========================
# UTILS
# =========================

def load_font(filename, size):
    path = resource_path(os.path.join("fonts", filename))
    if not os.path.exists(path):
        print(f"[WARN] No se encontró la fuente {path}, usando default")
        return ImageFont.load_default()
    return ImageFont.truetype(path, size)


def formatear_titulo_categoria(texto, max_chars=12):
    
    # Parte el texto en varias líneas automáticamente según la longitud.
   
    lineas = textwrap.wrap(texto, width=max_chars)
    return "\n".join(lineas)

# =========================
# LABELS DEL TABLERO
# =========================

def crear_label_categoria(parent, nombre):
    # Texto inicial visible
    label_img = tk.Label(
        parent,
        text=nombre,
        fg="white", # Esto asegura que el texto se vea mientras se genera la imagen dorada
        bg=BG_MAIN,
        font=("Orbitron", 14, "bold"), # Bajamos un poco el tamaño base para notebooks
        anchor="center",
        justify="center"
    )

    def generar(event=None):
        # Bajamos el margen de 10 a 5 para ganar espacio en pantallas chicas
        MAX_WIDTH = label_img.winfo_width() - 5
        MAX_HEIGHT = label_img.winfo_height() - 5
        
        # Bajamos el umbral de 50 a 20 para que se dispare más rápido en notebooks
        if MAX_WIDTH < 20 or MAX_HEIGHT < 20:
            label_img.after(100, generar)
            return

        MIN_FONT = 20
        MAX_FONT = 40
        nombre_formateado = nombre

        font_size_final = MIN_FONT
        for size in range(MAX_FONT, MIN_FONT - 1, -2):
            img_test = crear_texto_dorado(nombre_formateado, "fredoka.ttf", size)
            if img_test.width() <= MAX_WIDTH and img_test.height() <= MAX_HEIGHT:
                font_size_final = size
                break

        frames = [
            crear_texto_dorado(nombre_formateado, "fredoka.ttf", font_size_final, brillo_pos=i)
            for i in range(0, 120, 6)
        ]

        label_img.frames = frames
        label_img.frame_index = 0
        animar()

    def animar():
        if not hasattr(label_img, "frames"):
            return
        frame = label_img.frames[label_img.frame_index]
        label_img.config(image=frame, text="")  # reemplaza texto por imagen
        label_img.image = frame
        label_img.frame_index = (label_img.frame_index + 1) % len(label_img.frames)
        label_img.after(80, animar)

    label_img.bind("<Configure>", generar)
    return label_img



def crear_label_tiempo(parent, tiempo):
    return tk.Label(
        parent, 
        text=f"Tiempo: {tiempo}", 
        font=("Arial", 20),
        fg="red", 
        bg=BG_MAIN)


def crear_label_pregunta(parent, texto):
    return tk.Label(
        parent, 
        text=texto,  # texto de la pregunta
        font=("Arial", 30, "bold"), # tamaño y estilo de la letra
        fg="white", 
        bg=BG_MAIN, # fondo del rectangulo de la pregunta
        wraplength=900, #ancho máximo antes de hacer salto de línea
        justify="center")


def animar_bonus_canvas(self, canvas_destino):
    colores = ["#FFD700", "#FFC300", "#FFB347", "#FFE29A"]
    ancho_p = self.root.winfo_screenwidth()
    
    # Coordenadas: X al centro, Y un poco arriba del texto de puntos
    x, y = ancho_p // 2, 120
    texto = "🎁 ¡BONUS x2!"

    def actualizar_color(paso=0):
        # Si la ventana se cerró, cortamos la animación
        if not self.ventana_pregunta.winfo_exists():
            return

        # Borramos solo el texto del bonus usando un "tag"
        canvas_destino.delete("tag_bonus")

        # Dibujamos una pequeña sombra negra para que resalte sobre la foto
        canvas_destino.create_text(
            x + 2, y + 2, text=texto, font=("Orbitron", 32, "bold"),
            fill="black", tags="tag_bonus"
        )
        
        # Dibujamos el texto principal con el color animado
        canvas_destino.create_text(
            x, y, text=texto, font=("Orbitron", 32, "bold"),
            fill=colores[paso], tags="tag_bonus"
        )

        # Programamos el siguiente cambio de color
        siguiente = (paso + 1) % len(colores)
        self.ventana_pregunta.after(200, lambda: actualizar_color(siguiente))

    actualizar_color()

    
def crear_label_puntaje(parent, nombre):

    img = crear_boton_redondeado(
        nombre,
        240,
        100,
        "#1E90FF",   # azul base
        "#63B8FF"    # brillo
    )

    lbl = tk.Label(
        parent,
        image=img,
        text=f"{nombre}\n0",
        compound="center",
        font=("Orbitron", 14, "bold"),
        fg="white",
        bg=parent["bg"]
    )

    lbl.image = img
    return lbl


def crear_label_respuesta(parent, texto, color):
    return tk.Label(
        parent, 
        text=texto, 
        font=("Arial", 20, "bold"),
        fg=color, 
        bg=BG_MAIN)


def crear_label_respuesta_final(parent, texto):
    return tk.Label(parent, text=texto, font=("Arial", 18),
                    fg="white", bg=BG_MAIN)



# =========================
# LABEL FINAL DEL GANADOR
# =========================

def dibujar_interfaz_ganador(canvas, puntajes, ancho_p, alto_p):
    """
    Dibuja la pantalla de ganador directamente en el canvas.
    Solo texto, con título dorado y contorno negro fijo.
    """
    if not puntajes:
        canvas.create_text(
            ancho_p//2, alto_p//2,
            text="No hay puntajes",
            fill="white",
            font=("Arial", 30)
        )
        return

    # 1. Procesar datos
    jugadores_ordenados = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
    max_puntos = jugadores_ordenados[0][1]
    ganadores = [nombre for nombre, puntos in jugadores_ordenados if puntos == max_puntos]
    titulo_texto = "🏆 GANADOR 🏆" if len(ganadores) == 1 else "🏆 EMPATE 🏆"

    # 2. Dibujar título dorado
    canvas.create_text(
        (ancho_p // 2) + 3, (alto_p * 0.10) + 3,
        text=titulo_texto,
        font=("Orbitron", int(alto_p * 0.08), "bold"),
        fill="black", justify="center"
    )
    canvas.create_text(
        ancho_p // 2, alto_p * 0.10,
        text=titulo_texto,
        font=("Orbitron", int(alto_p * 0.08), "bold"),
        fill="#FFD700", justify="center"
    )

    # 3. Dibujar al Ganador/es (AJUSTADO PARA EMPATES)
    y_offset = alto_p * 0.25
    
    # Si hay empate, usamos un espaciado más grande entre cada bloque
    espaciado_ganadores = alto_p * 0.10 if len(ganadores) > 1 else alto_p * 0.15

    for nombre in ganadores:
        # Contorno negro
        canvas.create_text(
            (ancho_p // 2) + 3, y_offset + 3,
            text=f"{nombre.upper()} {max_puntos} PTS",
            font=("Orbitron", int(alto_p * 0.06), "bold"),
            fill="black", justify="center"
        )
        # Texto principal verde neón
        canvas.create_text(
            ancho_p // 2, y_offset,
            text=f"{nombre.upper()} {max_puntos} PTS",
            font=("Orbitron", int(alto_p * 0.06), "bold"),
            fill="#29FC45", justify="center"
        )
        # Aumentamos el offset con la nueva variable de separación
        y_offset += espaciado_ganadores

    # 4. Dibujar tabla de posiciones (CORREGIDO)
    
    y_lista = y_offset + 20 
    
    for nombre, puntos in jugadores_ordenados:
        if puntos < max_puntos:
            # Color rojo fuerte para todos los que no ganaron
            color_texto = "#FF3333" 
            
            # Dibujamos la SOMBRA SIEMPRE (quitamos el if puntos <= 0)
            canvas.create_text(
                (ancho_p // 2) + 2, y_lista + 2,
                text=f"{nombre}: {puntos} pts",
                font=("Arial", int(alto_p * 0.03), "bold"),
                fill="black", justify="center"
            )

            # Texto principal encima
            canvas.create_text(
                ancho_p // 2, y_lista,
                text=f"{nombre}: {puntos} pts",
                font=("Arial", int(alto_p * 0.03), "bold"),
                fill=color_texto, justify="center"
            )

            y_lista += 50
