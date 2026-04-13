import tkinter as tk
import random

from ui.styles import *

class EfectoMatrix:
    def __init__(self, parent, width, height):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        # 🔽 Mandamos el fondo atrás para no tapar botones
        self.canvas.lower("all")

        self.width = width
        self.height = height

        self.fuente = ("Consolas", 13, "bold")
        self.chars = list("EdujUegO2026")

        # grilla fija
        self.col_width = 15
        self.row_height = 18
        self.columnas = max(1, width // self.col_width)
        self.filas = height // self.row_height + 5

        self.streams = []
        for i in range(self.columnas):
            x = i * self.col_width
            stream = []
            for j in range(self.filas):
                y = j * self.row_height
                char = random.choice(self.chars)
                text_id = self.canvas.create_text(
                    x, y,
                    text=char,
                    fill=MATRIX_TAIL,
                    font=self.fuente,
                    anchor="nw"
                )
                stream.append(text_id)
            self.streams.append(stream)

        # offset inicial distinto por columna
        self.offsets = [random.randint(0, self.filas) for _ in range(self.columnas)]
        self.animar()

    def animar(self):
        for col_idx, stream in enumerate(self.streams):
            offset = self.offsets[col_idx]
            self.offsets[col_idx] = (offset + 1) % self.filas

            for row_idx, text_id in enumerate(stream):
                pos = (row_idx + offset) % self.filas
                char = random.choice(self.chars)

                # gradiente de color: cabeza brillante, cola oscura
                if pos == 0:
                    color = MATRIX_HEAD
                elif pos < 4:
                    color = MATRIX_MID
                else:
                    color = MATRIX_TAIL

                self.canvas.itemconfig(text_id, text=char, fill=color)

        # velocidad desde styles.py
        self.canvas.after(MATRIX_SPEED, self.animar)