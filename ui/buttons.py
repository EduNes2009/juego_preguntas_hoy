from utils import resource_path
from PIL import Image, ImageDraw, ImageFilter, ImageColor, ImageTk, ImageFont
import os
import tkinter as tk



def crear_boton_redondeado(texto, ancho, alto, color_base, color_brillo):
    factor = 4
    w, h = ancho * factor, alto * factor

    # Imagen base transparente
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # 1. Cuerpo ovalado del botón
    cuerpo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_c = ImageDraw.Draw(cuerpo)
    coords_cuerpo = [0, 0, w, h]
    draw_c.rounded_rectangle(coords_cuerpo, radius=h//2, fill=color_base)

    # 2. Resplandor interno
    cuerpo = cuerpo.filter(ImageFilter.GaussianBlur(radius=3 * factor))

    # 3. Gradiente vertical suave con máscara
    mascara = Image.new("L", (w, h), 0)
    mask_draw = ImageDraw.Draw(mascara)
    mask_draw.rounded_rectangle(coords_cuerpo, radius=h//2, fill=255)

    gradiente = Image.new("RGBA", (w, h))
    draw_grad = ImageDraw.Draw(gradiente)
    r_b, g_b, b_b = ImageColor.getrgb(color_base)
    r_br, g_br, b_br = ImageColor.getrgb(color_brillo)
    for y in range(h):
        ratio = y / h
        color = (
            int(r_b + (r_br - r_b) * ratio),
            int(g_b + (g_br - g_b) * ratio),
            int(b_b + (b_br - b_b) * ratio),
            255
        )
        draw_grad.line([(0, y), (w, y)], fill=color)

    gradiente.putalpha(mascara)
    img = gradiente
    img.paste(cuerpo, (0, 0), mask=mascara)

    # 4. Texto con sombra
    draw_texto = ImageDraw.Draw(img)
    try:
        font_path = resource_path(os.path.join("fonts", "fredoka.ttf"))
        fuente = ImageFont.truetype(font_path, int(20 * factor))  # tamaño mayor
    except:
        fuente = ImageFont.load_default()

    bbox = draw_texto.textbbox((0, 0), texto, font=fuente)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    # Sombra negra
    draw_texto.text(((w - tw) / 2 + 3*factor, (h - th) / 2 + 3*factor),
                    texto, font=fuente, fill="black")

    # Texto blanco encima
    draw_texto.text(((w - tw) / 2, (h - th) / 2),
                    texto, font=fuente, fill="white")

    # 5. Redimensionar al tamaño original
    img_final = img.resize((ancho, alto), Image.LANCZOS)
    return ImageTk.PhotoImage(img_final)




def crear_brillo_boton(canvas, x, y, ancho, alto, color_brillo):
    """
    Dibuja un aura neón ovalada directamente en el canvas.
    """
    # Crear una imagen transparente
    pad = 30
    img = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dibujar un óvalo/cápsula con el color del brillo
    coords = [pad//2, pad//2, ancho + pad//2, alto + pad//2]
    draw.ellipse(coords,  fill=color_brillo)
    
    # Aplicar desenfoque gaussiano más amplio para un resplandor suave
    img_desenfocada = img.filter(ImageFilter.GaussianBlur(radius=65))
    
    # Convertir a PhotoImage para Tkinter
    #global img_brillo_tk  # Necesitamos guardar la referencia
   # Dibujar la imagen de brillo en el canvas
    img_brillo_tk = ImageTk.PhotoImage(img_desenfocada)
    id_brillo = canvas.create_image(x, y, image=img_brillo_tk)
    
    # Devolver el ID y la referencia para que no se pierda
    return id_brillo, img_brillo_tk
