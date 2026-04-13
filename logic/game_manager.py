class GameManager:

    def __init__(self, score_manager):
        self.score_manager = score_manager
        self.turno_actual = 0
        self.jugadores = []
        self.pregunta_actual = None
        self.juego_terminado = False

    def agregar_jugadores(self, jugadores):
        self.jugadores = jugadores

    def jugador_actual(self):
        if not self.jugadores:
            return None
        return self.jugadores[self.turno_actual]

    def siguiente_turno(self):
        if not self.jugadores:
            return

        self.turno_actual += 1

        if self.turno_actual >= len(self.jugadores):
            self.turno_actual = 0

    def set_pregunta(self, pregunta):
        self.pregunta_actual = pregunta

    def responder_correcto(self, jugador, puntos):
        self.score_manager.actualizar_puntaje(jugador, puntos)

    def responder_incorrecto(self, jugador, puntos):
        self.score_manager.actualizar_puntaje(jugador, -puntos)

    def obtener_puntajes(self):
        return self.score_manager.obtener_todos()
    