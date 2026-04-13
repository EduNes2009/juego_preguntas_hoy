import pygame
from utils import resource_path


class AudioManager:
    def __init__(self):
        # Inicializar mixer UNA sola vez
        pygame.init()
        pygame.mixer.init()
        

        # Diccionario de sonidos
        self.sounds = {}

        # Estado música
        self.music_playing = None

    # ---------------------------
    # CARGAR SONIDO
    # ---------------------------
    def load_sound(self, name, path, volume=1.0):
        sound = pygame.mixer.Sound(resource_path(path))
        sound.set_volume(volume)
        self.sounds[name] = sound

    # ---------------------------
    # REPRODUCIR SONIDO
    # ---------------------------
    def play(self, name, loops =0):
        if name in self.sounds:
            self.sounds[name].play(loops=loops)

    # ---------------------------
    # REPRODUCIR MÚSICA
    # ---------------------------
    def play_music(self, path, volume=0.5, loop=True):
        pygame.mixer.music.load(resource_path(path))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1 if loop else 0)
        self.music_playing = path

    # ---------------------------
    # DETENER MÚSICA
    # ---------------------------
    def stop_music(self):
        pygame.mixer.music.stop()

    # ---------------------------
    # DETENER TODo
    # ---------------------------
    def stop_all(self):
        pygame.mixer.stop()

    # ---------------------------
    # CERRAR AUDIO
    # ---------------------------
    def quit(self):
        pygame.mixer.quit()
        pygame.quit()