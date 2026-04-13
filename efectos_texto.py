from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter
import os
from utils import resource_path
import tkinter as tk
from ui.styles import BG_PANEL

# -------------------------
# Texto dorado con copas
# -------------------------
def crear_texto_dorado_con_copas(texto, font_filename, size, brillo_pos=None):
    font_path = resource_path(os.path.join("fonts", font_filename))
    copa_path = resource_path(os.path.join("imagenes", "copa.png"))

    font = ImageFont.truetype(font_path, size)
    bbox = font.getbbox(texto)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    gradiente = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
    draw_grad = ImageDraw.Draw(gradiente)
    for y in range(text_h):
        ratio = y / text_h
        r = int(190 + 65 * ratio)
        g = int(150 + 80 * ratio)
        b = int(30 + 20 * ratio)
        draw_grad.line((0, y, text_w, y), fill=(r, g, b, 255))

    if brillo_pos is not None:
        brillo = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
        draw_brillo = ImageDraw.Draw(brillo)
        for y in range(text_h):
            alpha = max(0, 180 - abs(y - brillo_pos) * 4)
            if alpha > 0:
                draw_brillo.line((0, y, text_w, y), fill=(255, 255, 255, alpha))
        brillo = brillo.filter(ImageFilter.GaussianBlur(radius=2))
        gradiente = Image.alpha_composite(gradiente, brillo)

    mask = Image.new("L", (text_w, text_h), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.text((-bbox[0], -bbox[1]), texto, font=font, fill=255)
    texto_img = Image.composite(gradiente, Image.new("RGBA", (text_w, text_h)), mask)

    copa = Image.open(copa_path).convert("RGBA")
    copa_h = int(text_h * 1.1)
    copa_w = int(copa.width * (copa_h / copa.height))
    copa = copa.resize((copa_w, copa_h), Image.LANCZOS)

    separacion = 30
    total_w = text_w + copa_w * 2 + separacion * 2
    total_h = max(text_h, copa_h)

    base = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    x_texto = copa_w + separacion
    base.paste(texto_img, (x_texto, 0), texto_img)

    y_copa = (total_h - copa_h) // 2
    base.paste(copa, (0, y_copa), copa)
    base.paste(copa, (total_w - copa_w, y_copa), copa)

    return ImageTk.PhotoImage(base)

# -------------------------
# Texto dorado simple
# -------------------------
def crear_texto_dorado(texto, font_filename, size, brillo_pos=None):
    font_path = resource_path(os.path.join("fonts", font_filename))
    font = ImageFont.truetype(font_path, size)

    # 🔧 Soporte real para múltiples líneas
    lineas = texto.split("\n")
    bboxes = [font.getbbox(linea) for linea in lineas]

    anchos = [bbox[2] - bbox[0] for bbox in bboxes]
    altos = [bbox[3] - bbox[1] for bbox in bboxes]

    text_w = max(anchos) if anchos else 1
    line_h = max(altos) if altos else size
    text_h = line_h * len(lineas) + (len(lineas) - 1) * 6  # separación entre líneas

    # ✅ Padding real
    pad_top = int(size * 0.6)
    pad_bottom = int(size * 0.4)
    pad_x = 16

    img_w = text_w + pad_x * 2
    img_h = text_h + pad_top + pad_bottom

    gradiente = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw_grad = ImageDraw.Draw(gradiente)

    for y in range(img_h):
        ratio = y / img_h
        r = int(190 + 65 * ratio)
        g = int(150 + 80 * ratio)
        b = int(30 + 20 * ratio)
        draw_grad.line((0, y, img_w, y), fill=(r, g, b, 255))

    if brillo_pos is not None:
        brillo = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
        draw_brillo = ImageDraw.Draw(brillo)
        for y in range(img_h):
            alpha = max(0, 180 - abs(y - brillo_pos) * 4)
            if alpha > 0:
                draw_brillo.line((0, y, img_w, y), fill=(255, 255, 255, alpha))
        brillo = brillo.filter(ImageFilter.GaussianBlur(radius=2))
        gradiente = Image.alpha_composite(gradiente, brillo)

    mask = Image.new("L", (img_w, img_h), 0)
    draw_mask = ImageDraw.Draw(mask)

    # 🧠 Dibujar cada línea centrada
    y_cursor = pad_top
    for i, linea in enumerate(lineas):
        bbox = bboxes[i]
        w = bbox[2] - bbox[0]

        x = (img_w - w) // 2 - bbox[0]
        y = y_cursor - bbox[1]

        draw_mask.text((x, y), linea, font=font, fill=255)
        y_cursor += line_h + 6

    texto_img = Image.composite(gradiente, Image.new("RGBA", (img_w, img_h)), mask)

    return ImageTk.PhotoImage(texto_img)




# -------------------------
# Texto verde metálico (para ganadores)
# -------------------------
def crear_texto_verde_metalico(parent, texto):
    colores = ["#08774B", "#1C3D32", "#00CC77", "#33FFAA"]
    label = tk.Label(parent,
                     text=texto,
                     font=("Orbitron", 78, "bold"),
                     bg=BG_PANEL)
    label.place(relx=0.5, rely=0.5, anchor="center")


    indice = {"i": 0}
    def animar():
        label.config(fg=colores[indice["i"]])
        indice["i"] = (indice["i"] + 1) % len(colores)
        label.after(200, animar)
    animar()
    return label

# -------------------------
# Texto pregunta/respuesta
# -------------------------
def crear_texto_pregunta_respuesta(parent, texto, font=("Orbitron", 28, "bold"), color="#09692E", bg="#68E614"):
    label = tk.Label(parent, text=texto, font=font, fg=color, bg=bg)
    label.pack(pady=20)

    def animar(iteraciones=10):
        if iteraciones > 0:
            nuevo_color = color if iteraciones % 2 == 0 else "green"
            label.config(fg=nuevo_color)
            parent.after(200, lambda: animar(iteraciones - 1))
        else:
            label.config(fg=color)
    animar()
    return label

def crear_texto_verde_metalico_pack(parent, texto):
    colores = ["#00FF99", "#66FFCC", "#00CC77", "#33FFAA"]
    label = tk.Label(parent,
                     text=texto,
                     font=("Orbitron", 48, "bold"),
                     bg=BG_PANEL)
    label.pack(pady=10)   # ← pack en vez de place

    indice = {"i": 0}
    def animar():
        label.config(fg=colores[indice["i"]])
        indice["i"] = (indice["i"] + 1) % len(colores)
        label.after(200, animar)
    animar()
    return label

        
def crear_texto_verde_metalico_titulo(parent, texto):
    # calcular tamaño dinámico según alto de la ventana 
    alto = parent.winfo_height() 
    size = max(20, alto // 15)  # proporcional al alto, con mínimo 20
    
    return tk.Label(
        parent,
        text=texto,
        font=("Consolas", size, "bold"),
        fg="#00FF9C",              # verde metálico
        bg=None,           # mismo fondo → se ve transparente
        bd=0,                      # sin borde
        highlightthickness=0,      # sin resaltado
        relief="flat"              # evita marcos 3D
    )
