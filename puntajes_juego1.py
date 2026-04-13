class ScoreManager:
    def __init__(self):
        self.puntajes = {}

    def cargar_jugadores(self, archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    nombre = linea.strip()
                    if nombre:
                        self.puntajes[nombre] = 0
        except FileNotFoundError:
            print(f"No se encontró el archivo {archivo}")

    def agregar_jugador(self, nombre):
        if nombre not in self.puntajes:
            self.puntajes[nombre] = 0

    def actualizar_puntaje(self, nombre, puntos):
        if nombre in self.puntajes:
            self.puntajes[nombre] += puntos

    def obtener_puntaje(self, nombre):
        return self.puntajes.get(nombre, 0)

    def obtener_todos(self):
        return self.puntajes
    
    def reiniciar(self):
     self.puntajes.clear()