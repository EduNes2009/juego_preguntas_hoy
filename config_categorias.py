import tkinter as tk
import tkinter.messagebox as messagebox
import os

def ventana_categorias(root, callback_inicio):
    """
    Versión dinámica: Pregunta cantidades y configura el tablero 
    usando las preguntas existentes en la base de datos.
    """
    win = tk.Toplevel(root)
    win.title("Configurar Partida Dinámica")
    win.configure(bg="#0D1B2A")
    win.attributes("-fullscreen", True)

    # Permitir salir con Escape
    win.bind("<Escape>", lambda e: win.destroy())

    # Contenedor central para que se vea bien en pantalla completa
    main_frame = tk.Frame(win, bg="#1B263B", padx=50, pady=50, highlightbackground="#00FFF7", highlightthickness=2)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(main_frame, text="CONFIGURACIÓN DE TABLERO",
             font=("Orbitron", 24, "bold"), fg="#00FFF7", bg="#1B263B").pack(pady=(0, 30))

    # --- SELECTOR DE CATEGORÍAS (COLUMNAS) ---
    tk.Label(main_frame, text="¿Cuántas categorías quieres? (3 a 6)",
             font=("Arial", 16), fg="white", bg="#1B263B").pack(pady=5)
    
    cant_categorias_var = tk.IntVar(value=5)
    spin_cols = tk.Spinbox(main_frame, from_=3, to=6, textvariable=cant_categorias_var,
                           font=("Arial", 20, "bold"), width=5, justify="center",
                           buttonbackground="#00FFF7")
    spin_cols.pack(pady=10)

    # --- SELECTOR DE PREGUNTAS (FILAS) ---
    tk.Label(main_frame, text="¿Cuántas preguntas por categoría? (2 a 7)",
             font=("Arial", 16), fg="white", bg="#1B263B").pack(pady=5)
    
    cant_preguntas_var = tk.IntVar(value=5)
    spin_filas = tk.Spinbox(main_frame, from_=2, to=7, textvariable=cant_preguntas_var,
                            font=("Arial", 20, "bold"), width=5, justify="center",
                            buttonbackground="#00FFF7")
    spin_filas.pack(pady=10)

    def confirmar_configuracion():
        cols = cant_categorias_var.get()
        fils = cant_preguntas_var.get()

        # Validación de seguridad
        if not (3 <= cols <= 6) or not (2 <= fils <= 7):
            messagebox.showwarning("Límites", "Por favor mantente en los rangos: \nCols: 3-6\nFilas: 2-7")
            return

        # Cerramos esta ventana
        win.destroy()

        # PASO CLAVE: Pasamos las dimensiones al callback_inicio.
        # Aquí enviamos un diccionario con la configuración que el juego recibirá.
        config = {
            "modo": "dinamico",
            "columnas": cols,
            "filas": fils
        }
        
        # Llamamos al inicio del juego pasando esta data
        callback_inicio(config)

    # Botón de confirmación
    tk.Button(main_frame,
              text="¡COMENZAR JUEGO!",
              font=("Orbitron", 18, "bold"),
              bg="#00FFF7",
              fg="#0D1B2A",
              padx=30,
              pady=15,
              activebackground="white",
              command=confirmar_configuracion).pack(pady=40)

    # Instrucción para salir
    tk.Label(win, text="Presiona ESC para volver", font=("Arial", 10), 
             fg="gray", bg="#0D1B2A").pack(side="bottom", pady=10)