# ui/labels_intro.py
import tkinter as tk

def crear_label_titulo_config(parent):
    return tk.Label(parent,
                    text="🎮 CONFIGURAR JUGADORES",
                    font=("Orbitron", 18, "bold"),
                    fg="#00FFF7",
                    bg="#1B263B")

def crear_label_cantidad(parent):
    return tk.Label(parent,
                    text="¿Cuántos jugadores?",
                    font=("Roboto", 13, "bold"),
                    fg="white",
                    bg="#1B263B")

def crear_label_jugador(parent, numero):
    return tk.Label(parent,
                    text=f"Jugador {numero}",
                    font=("Roboto", 11, "bold"),
                    fg="white",
                    bg="#1B263B")
