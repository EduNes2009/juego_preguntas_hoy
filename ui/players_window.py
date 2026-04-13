import tkinter as tk

from logic.score_manager import ScoreManager
from ui.main_window import MainWindow

score_manager = ScoreManager()

class PlayersWindow(tk.Toplevel):
    def __init__(self, root, config_dinamica=None):
        super().__init__(root)
        self.config_dinamica = config_dinamica
        self.title("Jugadores")
        self.configure(bg="#1B263B")
        self.attributes("-fullscreen", True)

        self.entries = []
        self.jugadores = []

        tk.Label(self, text="¿Cuántos jugadores?", font=("Arial", 20, "bold"),
                 fg="white", bg="#1B263B").pack(pady=20)

        self.cantidad_entry = tk.Entry(
            self, font=("Arial", 16), justify="center",
            bg="white", fg="black", insertbackground="black"
        )
        vcmd = (self.register(self.validar_jugadores), "%P")
        self.cantidad_entry.config(validate="key", validatecommand=vcmd)
        self.cantidad_entry.pack(pady=10)
        self.cantidad_entry.insert(0, "2")
        
        # BOTÓN ACEPTAR
        self.btn_aceptar = tk.Button(self, text="Aceptar", command=self.crear_campos,
                                     font=("Arial", 14, "bold"), bg="#415A77", fg="white")
        self.btn_aceptar.pack(pady=10)

        # Solo bindeamos el Enter a la ventana después de un pequeño delay 
        # para evitar disparos accidentales al arrancar
        self.after(500, lambda: self.bind("<Return>", lambda e: self.btn_aceptar.invoke()))
        
        self.after(200, lambda: self.cantidad_entry.focus_set())

    def crear_campos(self):
        # Desvinculamos el Enter viejo para que no haya conflictos
        self.unbind("<Return>")
        
        for widget in self.entries:
            widget.destroy()
        self.entries.clear()

        try:
            cantidad = int(self.cantidad_entry.get())
        except ValueError:
            return

        for i in range(cantidad):
            entry = tk.Entry(self, font=("Arial", 14))
            entry.pack(pady=5)
            entry.insert(0, f"Jugador {i+1}")
            self.entries.append(entry)

        if self.entries:
            self.entries[0].focus()

        self.btn_comenzar = tk.Button(self, text="Comenzar juego", 
                                      command=self.guardar_jugadores,
                                      font=("Arial", 14, "bold"), 
                                      bg="#00FFF7", fg="black")
        self.btn_comenzar.pack(pady=20)

        # Re-bindeamos el Enter pero SOLO al botón comenzar ahora
        self.after(100, lambda: self.bind("<Return>", lambda e: self.btn_comenzar.invoke()))
  
    def guardar_jugadores(self):
        import traceback
        print("\n--- ¡ALERTA! Se disparó guardar_jugadores ---")
        
        
        try:
            # 1. Limpiamos y preparamos los datos
            self.jugadores.clear()
            
            # ⚠️ OJO ACÁ: Si lo pasaste por el __init__, debe ser self.score_manager
            if hasattr(self, 'score_manager'):
                self.score_manager.reiniciar()
            else:
                # Si es una variable global importada, asegúrate que se llame así
                print("Aviso: Usando score_manager global")
                score_manager.reiniciar() 

            for entry in self.entries:
                nombre = entry.get().strip()
                if nombre:
                    self.jugadores.append(nombre)
                    # Usamos self. si corresponde
                    if hasattr(self, 'score_manager'):
                        self.score_manager.agregar_jugador(nombre)
                    else:
                        score_manager.agregar_jugador(nombre)

            if not self.jugadores:
                print("No hay jugadores cargados.")
                return

            print(f"Jugadores listos: {self.jugadores}")

            # 2. Obtenemos la root
            root_principal = self.master
            
            # 3. Importamos el Tablero
            print("Importando MainWindow...")
            
            
            # 4. LANZAMOS EL TABLERO
            print("Ejecutando MainWindow...")
            MainWindow(
                root_principal, 
                self.jugadores, 
                self.score_manager if hasattr(self, 'score_manager') else score_manager, 
                callback_reinicio=self.reinicio_total, 
                config_dinamica=self.config_dinamica
            )
            
            print("MainWindow lanzado con éxito.")
            # 5. Cerramos la ventana de nombres
            self.destroy()

        except Exception as e:
            # ESTO TE VA A DECIR EL ERROR REAL EN CONSOLA
            print(f"CRASH en guardar_jugadores: {e}")

    def reinicio_total(self, *args):
        """ Función para que el juego pueda volver al inicio desde el main """
        from main import reiniciar_desde_main
        reiniciar_desde_main(self.master)

    def validar_jugadores(self, valor):
        """ Valida que el input sea un número entre 1 y 6 """
        if valor == "":
            return True
        if valor.isdigit() and 1 <= int(valor) <= 6:
            return True
        return False