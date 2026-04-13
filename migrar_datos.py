import json
import sqlite3
import os

# Rutas
ruta_json = "logic/data/questions.json"
ruta_db = "logic/data/preguntas_game.db"

def migrar():
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    # Asegurarnos que la tabla existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            pregunta TEXT,
            opcion_a TEXT,
            opcion_b TEXT,
            opcion_c TEXT,
            opcion_d TEXT,
            correcta TEXT,
            imagen TEXT,
            tipo TEXT
        )
    ''')

    for cat in data["categorias"]:
        nombre_cat = cat["nombre"]
        for p in cat["preguntas"]:
            # El JSON suele tener las opciones en una lista
            opc = p.get("opciones", ["", "", "", ""])
            cursor.execute('''
                INSERT INTO preguntas (categoria, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, correcta, imagen, tipo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nombre_cat, p["pregunta"], opc[0], opc[1], opc[2], opc[3], p["correcta"], p.get("imagen", ""), p.get("tipo", "texto")))

    conn.commit()
    conn.close()
    print("¡Migración completada con éxito!")

if __name__ == "__main__":
    migrar()