class ScoreManager:

    def __init__(self):
        self.puntajes = {}

    def reiniciar(self):
        self.puntajes.clear()

    def agregar_jugador(self, nombre):
        if nombre not in self.puntajes:
            self.puntajes[nombre] = 0

    def responder_correcto(self, jugador, puntos):
        if jugador in self.puntajes:
            self.puntajes[jugador] += puntos

    def responder_incorrecto(self, jugador, puntos):
        if jugador in self.puntajes:
            self.puntajes[jugador] -= puntos

    def obtener_puntaje(self, jugador):
        return self.puntajes.get(jugador, 0)

    def obtener_todos(self):
        return self.puntajes
    
    def actualizar_puntos(self, jugador, cantidad):
        """Suma o resta puntos al diccionario de puntajes"""
        if jugador in self.puntajes:
            self.puntajes[jugador] += cantidad
        else:
            # Por si el jugador no existe todavía
            self.puntajes[jugador] = cantidad