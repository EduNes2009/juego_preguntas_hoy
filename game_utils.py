import pygame

# Inicializar sonidos del juego
def init_sonidos():
    sonidos = {}
    pygame.mixer.init()
    sonidos["correcto"] = pygame.mixer.Sound("sounds/correcto.mp3")
    sonidos["incorrecto"] = pygame.mixer.Sound("sounds/incorrecto.mp3")
    sonidos["victoria"] = pygame.mixer.Sound("sounds/victoria.mp3")
    sonidos["timeout"] = pygame.mixer.Sound("sounds/timeout.mp3")
    return sonidos

# Reproducir sonido según resultado
def reproducir_sonido(sonidos, resultado):
    if resultado == "correcto":
        sonidos["correcto"].play()
    elif resultado == "incorrecto":
        sonidos["incorrecto"].play()
    elif resultado == "victoria":
        sonidos["victoria"].play()
    elif resultado == "timeout":
        sonidos["timeout"].play()