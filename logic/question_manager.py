import sqlite3
import os
import sys

def obtener_ruta_recurso(rel_path):
    """ Gestiona rutas para desarrollo (.py) y para el ejecutable (.exe) """
    if hasattr(sys, '_MEIPASS'):
        # Si es .exe, sys._MEIPASS es la raíz del paquete temporal
        return os.path.join(sys._MEIPASS, rel_path)
    # Si es .py, usamos la raíz de tu proyecto
    return os.path.join(os.path.abspath("."), rel_path)

class QuestionManager:
    def __init__(self):
        # USAMOS LA FUNCIÓN MÁGICA AQUÍ:
        # Esto buscará logic/data/preguntas_game.db correctamente en ambos mundos
        self.ruta_db = obtener_ruta_recurso(os.path.join("logic", "data", "preguntas_game.db"))
        
        print(f"DEBUG: Intentando abrir DB en: {self.ruta_db}")
        self.reiniciar_preguntas()

    def conectar(self):
        # Ahora self.ruta_db ya tiene la ruta absoluta correcta
        return sqlite3.connect(self.ruta_db)

    def reiniciar_preguntas(self):
        """Resetea las preguntas solo si quedan pocas disponibles."""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM preguntas WHERE usada = 0")
            cantidad_libre = cursor.fetchone()[0]

            # Si quedan menos de las necesarias para un tablero (42), reseteamos
            if cantidad_libre < 42: 
                print("Pocas preguntas libres. Reseteando base de datos...")
                cursor.execute("UPDATE preguntas SET usada = 0")
                conn.commit()
            
            conn.close()
            print("--- Base de datos lista para jugar ---")
        except Exception as e:
            print(f"Error al reiniciar preguntas: {e}")

    def obtener_pregunta(self, categoria, valor):
        """Busca una pregunta de la categoría sin importar el valor."""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            
            # 1. ACTUALIZA ESTA LÍNEA: Quitamos "AND puntos=?"
            # Ahora solo hay UN signo de pregunta
            query = "SELECT * FROM preguntas WHERE categoria=? AND usada=0 ORDER BY RANDOM() LIMIT 1"
            
            # 2. ACTUALIZA ESTA LÍNEA: Solo pasamos la categoría en la tupla
            cursor.execute(query, (categoria,)) 
            row = cursor.fetchone()
            
            # 3. Si no hay preguntas, reseteamos toda la categoría (sin filtrar por puntos)
            if not row:
                print(f"Reseteando disponibilidad para la categoría: {categoria}")
                cursor.execute("UPDATE preguntas SET usada=0 WHERE categoria=?", (categoria,))
                conn.commit()
                
                # Reintentamos
                cursor.execute(query, (categoria,))
                row = cursor.fetchone()

            if row:
                # Marcamos como usada usando su ID único
                cursor.execute("UPDATE preguntas SET usada=1 WHERE id=?", (row[0],))
                conn.commit()
                conn.close()
                
                return {
                    "id": row[0],
                    "pregunta": row[2],
                    "opciones": [row[3], row[4], row[5], row[6]],
                    "correcta": row[7],
                    "imagen": row[8],
                    "audio": row[9],
                    "tipo": row[10]
                }
            
            conn.close()
            return None
        except Exception as e:
            print(f"💥 ERROR en obtener_pregunta: {e}")
            return None

    def obtener_categorias(self):
        """Obtiene las categorías directamente de la DB."""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT categoria FROM preguntas")
            cats = [fila[0] for fila in cursor.fetchall()]
            conn.close()
            return cats
        except:
            return []

    def obtener_valores(self, cantidad_filas):
        """Genera la lista de valores según cuántas filas eligió el usuario."""
        valores_base = [100, 200, 300, 400, 500, 600, 700]
        # Devolvemos solo los que necesitamos (si eligió 3, devuelve [100, 200, 300])
        return valores_base[:cantidad_filas]

    def todas_respondidas(self, total_casillas_tablero, casillas_actuales):
        """
        Determina si el juego terminó comparando las casillas usadas 
        en el tablero contra el total (ej. 42).
        """
        return casillas_actuales >= total_casillas_tablero

    def resetear_estado_usadas(self):
        """Fuerza el reseteo manual de todas las preguntas."""
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE preguntas SET usada = 0")
        conn.commit()
        conn.close()
        print("--- TODAS LAS PREGUNTAS MARCADAS COMO NUEVAS ---")

    def marcar_respondida(self, categoria, valor):
        """Marca una pregunta como usada aunque no haya sido respondida (por tiempo agotado)."""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            # Marcamos como usada la última pregunta de esa categoría y puntaje
            # (Usamos LIMIT 1 por seguridad, aunque la lógica de obtener_pregunta ya lo hace)
            cursor.execute(
                "UPDATE preguntas SET usada = 1 WHERE categoria = ? AND puntos = ? AND usada = 0",
                (categoria, valor)
            )
            conn.commit()
            conn.close()
            print(f"--- Pregunta de {categoria} ({valor} pts) marcada como respondida por tiempo ---")
        except Exception as e:
            print(f"Error en marcar_respondida: {e}")
