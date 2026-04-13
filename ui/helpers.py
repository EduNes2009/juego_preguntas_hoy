


import tkinter as tk

def crear_rectangulo_redondeado(canvas, x1, y1, x2, y2, radio=25, **kwargs):
    puntos = [
        x1+radio, y1,
        x2-radio, y1,
        x2, y1,
        x2, y1+radio,
        x2, y2-radio,
        x2, y2,
        x2-radio, y2,
        x1+radio, y2,
        x1, y2,
        x1, y2-radio,
        x1, y1+radio,
        x1, y1
    ]
    return canvas.create_polygon(puntos, smooth=True, **kwargs)

def crear_fondo_degradado(canvas, width, height, color1="#3498DB", color2="#2C3E50"):
    # color1 = arriba, color2 = abajo
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)

    r_ratio = (r2 - r1) / height
    g_ratio = (g2 - g1) / height
    b_ratio = (b2 - b1) / height

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
        canvas.create_line(0, i, width, i, fill=color)
