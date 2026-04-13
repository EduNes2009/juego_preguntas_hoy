import tkinter as tk
from tkinter import messagebox
from ctypes import windll # Importas la herramienta

# 1. Configuras el DPI (ANTES de crear la ventana)
try:
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
import pygame
import time
import random
from PIL import Image, ImageTk
import os
import sys
    # --- CONFIGURACIÓN GLOBAL ---
try:
    RESAMPLING = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLING = Image.LANCZOS
    # --- IMPORTS INTERNOS ---
from utils import resource_path
from ui.buttons import crear_boton_redondeado, crear_brillo_boton
from ui.labels import crear_label_categoria, crear_label_tiempo, dibujar_interfaz_ganador
from ui.styles import *
from ui.helpers import crear_rectangulo_redondeado, crear_fondo_degradado

from logic.score_manager import ScoreManager
from logic.game_manager import GameManager
from logic.question_manager import QuestionManager
from audio.audio_manager import AudioManager

# --- FUNCIÓN PARA BLINDAR RUTAS (EXTERNO/INTERNO) ---
def obtener_ruta_recurso(carpeta, archivo):
    """
    Busca primero en la carpeta externa (pendrive/dist) 
    y si no existe, usa el recurso interno del .exe.
    """
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    ruta_externa = os.path.join(base_dir, carpeta, archivo)
    
    if os.path.exists(ruta_externa):
        return ruta_externa
    return resource_path(os.path.join(carpeta, archivo))

class MainWindow:
    def __init__(self, root, jugadores, score_manager, callback_reinicio=None, config_dinamica=None):
        # 1. Atributos Básicos
        self.root_base = root
        self.jugadores = jugadores
        self.score_manager = score_manager
        self.game_manager = GameManager(self.score_manager)
        self.game_manager.agregar_jugadores(jugadores)
        self.question_manager = QuestionManager()
        self.callback_reinicio = callback_reinicio

        # 2. Configuración de Filas y Columnas
        if config_dinamica:
            todas_las_cats = self.question_manager.obtener_categorias()
            self.categorias = todas_las_cats[:config_dinamica["columnas"]]
            self.valores = [100 * (i + 1) for i in range(config_dinamica["filas"])]
            self.cantidad_bonus = 9
        else:
            self.categorias = self.question_manager.obtener_categorias()
            self.valores = self.question_manager.obtener_valores()
            self.cantidad_bonus = 9

        self.bonus_x2 = set()
        self.preparar_bonus()

        # 3. Preparación de Diccionarios y Estados
        self.botones_tablero = {}
        self.labels_puntajes = {}
        self.botones_jugadores = {}
        self.casillas_usadas = set()
        self.tiempo_total = 30
        self.timer_activo = False
        self.timer_id = None
        self.intervalo_animacion = 50
        self.barra_progresiva = None
        self.tiempo_revelacion = 5000 
        self.bg_pregunta = None


        self.root = tk.Toplevel(root)
        self.root.title("Juego")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=BG_MAIN)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.canvas_fondo = tk.Canvas(self.root, bg="#001a00", highlightthickness=0)
        self.canvas_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        #  Audio
        self.audio = AudioManager()
        self.audio.load_sound("correcto", resource_path("sounds/correcto.mp3"), volume=0.7)
        self.audio.load_sound("incorrecto", resource_path("sounds/incorrecto.mp3"), volume=0.7)
        self.audio.load_sound("victoria", resource_path("sounds/victoria.mp3"), volume=0.8)
        self.audio.load_sound("timeout", resource_path("sounds/timeout.mp3"), volume=0.7)
        self.audio.load_sound("bonus", resource_path("sounds/bonus.mp3"), volume=0.8)
        self.audio.load_sound("warning", resource_path("sounds/warning.mp3"), volume=0.5)
        self.sonido_click = pygame.mixer.Sound(resource_path("sounds/Casilla.mp3"))
        self.sonido_click.set_volume(0.2)

        #  Estructura de Frames (corregido)
        self.frame_central = tk.Frame(self.root, bg=BG_MAIN)
        self.frame_central.grid(row=0, column=0, sticky="nsew")

        # Tablero de categorías/preguntas
        self.frame_central = tk.Frame(self.root, bg=BG_MAIN)
        self.frame_central.grid(row=0, column=0, sticky="nsew")

        # IMPORTANTE: El frame_tablero NO debe tener sticky="nsew" para poder centrarse
        self.frame_tablero = tk.Frame(self.frame_central, bg=BG_MAIN)
        self.frame_tablero.grid(row=0, column=0, sticky="n") # "n" para que esté arriba pero centrado

        self.frame_panel = tk.Frame(self.frame_central, bg=BG_MAIN)
        self.frame_panel.grid(row=1, column=0, sticky="ew")

        # Configurar pesos del contenedor principal
        self.frame_central.grid_rowconfigure(0, weight=1) # El tablero se expande
        self.frame_central.grid_rowconfigure(1, weight=0) # El panel de abajo es fijo
        self.frame_central.grid_columnconfigure(0, weight=1) # Centra horizontalmente

        # 8. Lanzamiento
        self.run()
        self.root.bind("<Escape>", lambda e: self.cerrar_juego())
        self.root.update_idletasks()
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        self.root = root
     
         # 1. Inicializar el mezclador
        pygame.mixer.init()
        
        # 2. Cargar el sonido (Usamos os.path para que sea compatible con carpetas)
        ruta_sonido = os.path.join("assets", "harry_potter1.mp3") 
        try:
            self.hp_sound = pygame.mixer.Sound(ruta_sonido)
        except:
            print("No se encontró el archivo de sonido, el juego seguirá sin audio.")
            self.hp_sound = None


    def preparar_bonus(self):
        """Genera 9 bonus aleatorios basados en las casillas actuales."""
        todas_las_casillas = []
        for c in self.categorias:
            for v in self.valores:
                todas_las_casillas.append((c, v))
        
        # Tomamos 9 muestras sin repetir
        cantidad = min(self.cantidad_bonus, len(todas_las_casillas))
        self.bonus_x2 = set(random.sample(todas_las_casillas, cantidad))
        print(f"DEBUG: 9 Bonus generados en: {self.bonus_x2}")

    def run(self):
        self.crear_panel_inferior()
        self.reproducir_musica_fondo()
        self.crear_tablero()

    def reproducir_musica_fondo(self):
        try:
            # Usamos la ruta que ya tenés definida
            ruta = resource_path("sounds/Holiday-Weasel.mp3") 
            
            if os.path.exists(ruta):
                pygame.mixer.music.load(ruta)
                pygame.mixer.music.set_volume(0.3) # 0.5 puede ser un poco alto si hay voces
                pygame.mixer.music.play(-1)
                print("🎵 Música de fondo reanudada.")
            else:
                print(f"⚠️ Archivo no encontrado en: {ruta}")
        except Exception as e:
            print("Error al cargar música de fondo:", e)

    def cerrar_juego(self):
        print("CERRANDO TODO...")

        # 🧹 cancelar timers
        try:
            self.cancelar_timers()
        except:
            pass

        # 🔊 cerrar pygame
        try:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            pygame.mixer.quit()
            pygame.quit()
        except Exception as e:
            print("Error pygame:", e)

        # 🪟 cerrar ventanas hijas
        try:
            if hasattr(self, "ventana_pregunta") and self.ventana_pregunta.winfo_exists():
                self.ventana_pregunta.destroy()
        except:
            pass

        try:
            if hasattr(self, "ventana_final") and self.ventana_final.winfo_exists():
                self.ventana_final.destroy()
        except:
            pass

        # 🪟 cerrar ventana principal del juego
        try:
            self.root.destroy()
        except:
            pass

        # 🧨 cerrar root base (CLAVE)
        try:
            self.root_base.destroy()
        except:
            pass

        # 💣 cerrar proceso completamente
        os._exit(0)

    def crear_tablero(self):
        # 1. Limpieza inicial
        if hasattr(self, "tablero"):
            self.tablero.destroy()

        # 2. Configuración del contenedor PADRE (Centrado)
        # Esto asegura que el frame_tablero sepa centrar a su hijo
        self.frame_tablero.grid_rowconfigure(0, weight=1)
        self.frame_tablero.grid_columnconfigure(0, weight=1)

        # 3. Creación del TABLERO (Solo una vez)
        # QUITAMOS "nsew" para que no se estire a lo ancho y se mantenga al centro
        self.tablero = tk.Frame(self.frame_tablero, bg=BG_MAIN)
        self.tablero.grid(row=0, column=0, sticky="n") # "n" lo mantiene arriba pero centrado

        # 4. Configuración de PESOS dinámicos
        total_filas = len(self.valores) + 1
        for i in range(total_filas):
            if i == 0:
                self.tablero.grid_rowconfigure(i, weight=3, minsize=70) 
            else:
                self.tablero.grid_rowconfigure(i, weight=4)

        for c in range(len(self.categorias)):
            # 'uniform' es clave para que todas las celdas midan lo mismo
            self.tablero.grid_columnconfigure(c, weight=1, uniform="columna")

        # 5. Carga y recorte de imagen (Lógica de fragmentos)
        ruta_fondo = resource_path(os.path.join("imagenes", "artemisAme.png"))
        imagen = Image.open(ruta_fondo)
        ancho, alto = imagen.size
        
        columnas = len(self.categorias) if len(self.categorias) > 0 else 1
        filas = len(self.valores) if len(self.valores) > 0 else 6

        ancho_celda_img = ancho // columnas
        alto_celda_img = alto // filas

        self.fragmentos = {}
        
        # 6. Creación de Contenido (Títulos y Casillas)
        for col, categoria in enumerate(self.categorias):
            # TÍTULOS (Fila 0)
            lbl_cat = crear_label_categoria(self.tablero, categoria)
            lbl_cat.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
            
            for fila, valor in enumerate(self.valores):
                # Recorte de la imagen de fondo
                self.fragmentos[(categoria, valor)] = imagen.crop((
                    col * ancho_celda_img, 
                    fila * alto_celda_img, 
                    (col + 1) * ancho_celda_img, 
                    (fila + 1) * alto_celda_img
                ))

                # Crear cada Casilla (Canvas)
                canvas = tk.Canvas(self.tablero, bg=BG_MAIN, highlightthickness=0)
                canvas.grid(row=fila+1, column=col, padx=2, pady=2, sticky="nsew")
                
                canvas.coord_EduJuegos = (categoria, valor)
                canvas.bind("<Button-1>", lambda e, cv=canvas, c=categoria, v=valor: self.click_casilla(cv, c, v))

                self.botones_tablero[(categoria, valor)] = {
                    "canvas": canvas, 
                    "imagen": self.fragmentos[(categoria, valor)]
                }

                # Función de dibujo interna
                def dibujar(event, cv=canvas):
                    cv.delete("all")
                    w, h = cv.winfo_width(), cv.winfo_height()
                    if w < 20 or h < 20: return
                    
                    cat_id, val_id = cv.coord_EduJuegos
                    if (cat_id, val_id) in self.casillas_usadas:
                        img_tk = self.imagenes_cache.get((cat_id, val_id))
                        if img_tk:
                            cv.create_image(w//2, h//2, anchor="center", image=img_tk)
                    else:
                        tamano_fuente = max(12, int(h * 0.35))
                        crear_rectangulo_redondeado(cv, 2, 2, w-2, h-2, radio=10, fill=BTN_NORMAL_BG, outline=BTN_BORDE_COLOR, width=2)
                        cv.create_text(w//2, h//2, text=f"{val_id}", fill=BTN_FG, font=("Orbitron", tamano_fuente, "bold"))

                canvas.bind("<Configure>", dibujar)

        # 5. Forzado de renderizado
        self.tablero.update()
        self.root.after(100, self.redimensionar_imagenes_final)

        # 5. Finalización y redimensionado inicial
        self.tablero.update_idletasks()
        self.root.after(100, self.redimensionar_imagenes_final)

    def redimensionar_imagenes_final(self):
            """ Nueva función para que no se trabe el tablero al inicio """
            self.imagenes_cache = {}
            
            for (categoria, valor), data in self.botones_tablero.items():
                cv, fragmento = data["canvas"], data["imagen"]
                
                # --- AGREGAMOS ESTA VERIFICACIÓN ---
                try:
                    # Si el canvas ya no existe (ventana cerrada), saltamos al siguiente
                    if not cv.winfo_exists():
                        continue
                    
                    w, h = cv.winfo_width(), cv.winfo_height()
                    
                    # Si el tamaño es muy chico, esperamos a que Tkinter termine de dibujar
                    if w <= 10 or h <= 10:
                        continue

                    img = fragmento.resize((w, h), Image.Resampling.LANCZOS)
                    self.imagenes_cache[(categoria, valor)] = ImageTk.PhotoImage(img)
                    
                    # Forzamos el dibujado de la imagen ya ganada
                    if (categoria, valor) in self.casillas_usadas:
                        cv.delete("all")
                        cv.create_image(w//2, h//2, anchor="center", image=self.imagenes_cache[(categoria, valor)])
                
                except Exception as e:
                    # Si hay cualquier error con un botón, lo ignoramos y seguimos con el resto
                    print(f"Aviso: No se pudo redimensionar casilla {categoria} {valor}")
                    continue

    def click_casilla(self, canvas, categoria, valor):
        # 1. Verificación básica
        if (categoria, valor) in self.casillas_usadas:
            return
            
        self.sonido_click.play()
        pygame.mixer.music.set_volume(0.2)
        
        # 2. Lógica de Puntos Sencilla
        puntos_base = int(valor)
        
        # El premio es doble SOLO si la casilla está en la lista de 9 bonus aleatorios
        # (Quitamos la lógica de la última fila para evitar errores de DB)
        if (categoria, valor) in self.bonus_x2:
            puntos_premio = puntos_base * 2
        else:
            puntos_premio = puntos_base

        # 3. Cambio visual en el tablero
        canvas.config(bg="#00aa00")
        
        # 4. Llamada a la función que ya tienes (con el lambda seguro)
        canvas.after(200, lambda c=categoria, b=puntos_base, p=puntos_premio: [
            pygame.mixer.music.set_volume(1.0), 
            self.abrir_pregunta(c, b, p)
        ])

    def crear_panel_inferior(self):
        if hasattr(self, "panel"): self.panel.destroy()
        
        self.panel = tk.Frame(self.frame_panel, bg=BG_MAIN)
        self.panel.pack(expand=True, fill="x")
        
        alto_pantalla = self.root.winfo_screenheight()
        es_notebook = alto_pantalla < 900 
        
        fuente_size = 18 if es_notebook else 24
        ancho_w = 220 if not es_notebook else 180
        alto_h = 100 if not es_notebook else 80

        for i, nombre in enumerate(self.jugadores):
            self.panel.grid_columnconfigure(i, weight=1)
            
            frame_contenedor = tk.Frame(self.panel, bg=BG_MAIN, cursor="hand2")
            frame_contenedor.grid(row=0, column=i, padx=10, pady=10, sticky="n")

            cv = tk.Canvas(
                frame_contenedor, 
                width=ancho_w, 
                height=alto_h, 
                bg=BG_MAIN, 
                highlightthickness=0
            )
            cv.pack()

            # IMPORTANTE: Le agregamos el tag "marco" para poder cambiarle el color después
            crear_rectangulo_redondeado(
                cv, 4, 4, ancho_w-4, alto_h-4, 
                radio=15, fill="#0a0a0a", outline="#FFD700", width=3,
                tags="marco" 
            )

            # 1. EL DEL PUNTAJE (Agregamos el replace en el tag)
            cv.create_text(
                ancho_w // 2, alto_h // 2 - 12,
                text="0",
                fill="#FFD700",
                font=("Orbitron", fuente_size + 6, "bold"),
                tags=f"puntos_{nombre.replace(' ', '_')}" # <-- CAMBIO AQUÍ
            )

            # 2. EL DEL NOMBRE (Se queda igual, es solo estético)
            cv.create_text(
                ancho_w // 2, alto_h // 2 + 22,
                text=nombre.upper(),
                fill="white",
                font=("Orbitron", fuente_size - 6, "bold")
            )

            cv.bind("<Button-1>", lambda e, n=nombre: self.seleccionar_jugador(n))
            
            self.labels_puntajes[nombre] = cv
            self.botones_jugadores[nombre] = cv

    def seleccionar_jugador(self, nombre=None):
        if nombre is None or isinstance(nombre, tk.Event):
            self.game_manager.turno_actual = (self.game_manager.turno_actual + 1) % len(self.game_manager.jugadores)
            nombre = self.game_manager.jugadores[self.game_manager.turno_actual]
        else:
            self.game_manager.turno_actual = self.game_manager.jugadores.index(nombre)
        
        # Color dorado base para los inactivos
        COLOR_BASE = "#FFD700"
        # Color de resaltado (el que ya venías usando para el borde)
        color_resaltado = PASTEL_NORMAL if 'PASTEL_NORMAL' in globals() else "#00FFFF" 

        for j_nombre, cv in self.botones_jugadores.items():
            # Limpiamos el nombre para el tag (por si tiene espacios)
            tag_puntos = f"puntos_{j_nombre.replace(' ', '_')}"
            
            if j_nombre == nombre:
                # JUGADOR ACTIVO: Borde más grueso y número del mismo color
                cv.itemconfig("marco", outline=color_resaltado, width=5)
                cv.itemconfig(tag_puntos, fill=color_resaltado)
            else:
                # JUGADORES INACTIVOS: Borde normal y número dorado
                cv.itemconfig("marco", outline=COLOR_BASE, width=3)
                cv.itemconfig(tag_puntos, fill=COLOR_BASE)

        print(f"Turno de: {nombre}")

    def abrir_pregunta(self, categoria, valor, premio_personalizado=None):
    
        puntos_busqueda = int(valor)
        
        # El premio que se suma al score (puede ser el doble)
        self.puntos_actuales = int(premio_personalizado) if premio_personalizado else puntos_busqueda
        
        # Guardamos en la clase para usar después al verificar respuesta
        self.categoria_actual = categoria
        self.valor_actual = puntos_busqueda # IMPORTANTE: Guardamos el original (ej. 500)
        
        jugador = self.game_manager.jugador_actual()
        if not jugador:
            messagebox.showwarning("Atención", "Seleccioná un jugador")
            return

        datos = self.question_manager.obtener_pregunta(categoria, puntos_busqueda)
        
        if datos is None:
            # Si entra acá, es porque realmente no hay preguntas de 500 en la DB
            messagebox.showwarning("Atención", f"No hay más preguntas de {categoria} por {puntos_busqueda} puntos.")
            return

        if categoria == "HARRY POTTER":
            try:
                # Usamos mixer.music para que no se solape con otros efectos cortos
                ruta_hp = obtener_ruta_recurso("sounds", "harry_potter1.mp3")
                pygame.mixer.music.load(ruta_hp)
                pygame.mixer.music.play() # Reproduce el tema al abrir la pregunta
            except Exception as e:
                print(f"No se pudo reproducir el tema de HP: {e}")    
      

        es_musica = (datos.get("tipo", "") == "musica")
        self.sonido_pregunta = None
        self.pregunta_actual, self.respuesta_actual = datos["pregunta"], datos["correcta"]
        
        # El Bonus visual (estrella dorada) se activa si el premio es mayor al valor base
        self.bonus_activo = self.puntos_actuales > puntos_busqueda

        # --- Ventana de la pregunta (sin cambios) ---
        self.ventana_pregunta = tk.Toplevel(self.root)
        self.ventana_pregunta.attributes("-fullscreen", True)
        self.ventana_pregunta.lift()
        self.ventana_pregunta.focus_force()
        self.ventana_pregunta.grab_set()
        ancho_p, alto_p = self.root.winfo_screenwidth(), self.root.winfo_screenheight()

        self.canvas_pregunta_fondo = tk.Canvas(self.ventana_pregunta, highlightthickness=0, bd=0)
        self.canvas_pregunta_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        # --- Fondo ---
        try:
            # Diccionario que vincula el nombre de la categoría con su imagen
            # IMPORTANTE: El nombre debe coincidir exactamente con el de la base de datos
            fondos_por_categoria = {
                "HARRY POTTER": "harry_potter1.png",
                "GEOGRAFÍA": "geografia.png",
                "CINE": "cine.png",
                "MÚSICA": "musica.png",
                "CIENCIA": "ciencia.png",
                "DEPORTES": "deporte.png"
            }

            # Buscamos la imagen en el diccionario. 
           
            nombre_archivo_fondo = fondos_por_categoria.get(categoria, "Templo.png")
            
            # Cargamos y procesamos la imagen
            img_path = obtener_ruta_recurso("imagenes", nombre_archivo_fondo)
            img_fondo = Image.open(img_path).resize((ancho_p, alto_p), Image.Resampling.LANCZOS)
            self.bg_pregunta = ImageTk.PhotoImage(img_fondo)
            
            # Dibujamos en el canvas
            self.canvas_pregunta_fondo.create_image(0, 0, image=self.bg_pregunta, anchor="nw")
            self.canvas_pregunta_fondo.image = self.bg_pregunta 
            
        except Exception as e:
            print(f"Error cargando fondo para {categoria}: {e}")
            self.canvas_pregunta_fondo.config(bg="#000a00")

        self.x_barra_inicio, self.y_barra_top = (ancho_p // 2) - 400, 80

        # --- AUDIO AUTOMÁTICO ---
        if es_musica:
            try:
                ruta_audio = obtener_ruta_recurso("sounds", datos["audio"])
                pygame.mixer.music.load(ruta_audio)
                
                # Reproducimos directamente sin esperar al botón
                # Usamos tu método existente para mantener cualquier efecto que tengas programado
                self.reproducir_con_efecto() 
                
                print(f"Reproduciendo automáticamente: {datos['audio']}")
            except Exception as e:
                print(f"Error al reproducir audio automático: {e}")

       
        # --- Texto de puntos ---
        if self.bonus_activo:
            texto_puntos = f"BONUS x 2\n⭐ ¡JUEGA POR {self.puntos_actuales} PUNTOS! ⭐"
            color_puntos = "#FFD700"  # dorado para bonus
        else:
            texto_puntos = f"JUEGA POR {self.puntos_actuales} PUNTOS"
            color_puntos = "#2AF145"  # verde normal

        # sombra opcional (negra, desplazada)
        self.canvas_pregunta_fondo.create_text(
            ancho_p // 2 + 2, 202,
            text=texto_puntos,
            font=("Orbitron", 40, "bold"),
            fill="black",
            width=ancho_p * 0.9,
            justify="center"
        )

        # texto principal en color
        self.canvas_pregunta_fondo.create_text(
            ancho_p // 2, 200,
            text=texto_puntos,
            font=("Orbitron", 40, "bold"),
            fill=color_puntos,
            width=ancho_p * 0.9,
            justify="center"
        )

        # --- Texto de la pregunta (CON SOMBRA) ---
        # Primero la sombra (un poquito desplazada a la derecha y abajo)
        self.canvas_pregunta_fondo.create_text(
            ancho_p // 2 + 3, alto_p * 0.58 + 3,
            text=self.pregunta_actual,
            font=("Orbitron", 40, "bold"),
            fill="black",  # Sombra negra
            width=ancho_p * 0.9,
            justify="center"
        )

        # Luego el texto principal en blanco
        self.canvas_pregunta_fondo.create_text(
            ancho_p // 2, alto_p * 0.58,
            text=self.pregunta_actual,
            font=("Orbitron", 40, "bold"),
            fill="white",  # Texto blanco
            width=ancho_p * 0.9,
            justify="center"
        )


        # --- Opciones ---
        ancho_btn, alto_btn, espacio = 500, 85, 40
        x_ini, y_ini = (ancho_p - (ancho_btn * 2 + espacio)) // 2, alto_p * 0.72
        for i, opcion in enumerate(datos["opciones"]):
            x, y = x_ini + (i % 2 * (ancho_btn + espacio)), y_ini + (i // 2 * (alto_btn + 20))
            c_opt = tk.Canvas(self.ventana_pregunta, width=ancho_btn, height=alto_btn, bg="#000a00", highlightthickness=0, bd=0)
            c_opt.place(x=x, y=y)
            crear_rectangulo_redondeado(c_opt, 0, 0, ancho_btn, alto_btn, radio=10, fill="#052505", outline="#00FFC8", width=3)
            c_opt.create_text(ancho_btn // 2, alto_btn // 2, text=f"{chr(65+i)}) {opcion}",
                            font=("Orbitron", 18, "bold"), fill="white", width=ancho_btn - 40, justify="center")
            c_opt.bind("<Button-1>", lambda e, r=opcion: self.verificar_respuesta(r))

        self.timer_activo = True
        self.inicio_timer = time.time()
        self.actualizar_timer()


    def reproducir_con_efecto(self):
        try:
            # No cargamos nada nuevo aquí porque ya se cargó en abrir_pregunta
            pygame.mixer.music.set_volume(0.8) 
            
            # CAMBIO 1: Agregamos -1 para que sea un bucle infinito
            pygame.mixer.music.play(-1) 
            
            # CAMBIO 2: Comentamos o borramos la línea que detiene la música a los 10 segundos
            # self.root.after(10000, self._detener_suavemente)
            
            print("🔊 Reproduciendo música en loop durante la pregunta...")
        except Exception as e:
            print("Error al reproducir:", e)

    def _detener_suavemente(self):
        # Detiene el audio de la pregunta
        pygame.mixer.music.stop()


    def animar_bonus_canvas(self, canvas_destino):
        colores = ["#FFD700", "#FFC300", "#FFB347", "#FFE29A"]
        x, y = self.root.winfo_screenwidth() // 2, 120
        def actualizar_color(paso=0):
            if not hasattr(self, "ventana_pregunta") or not self.ventana_pregunta.winfo_exists(): return
            canvas_destino.delete("tag_bonus")
            canvas_destino.create_text(x + 2, y + 2, text="🎁 ¡BONUS x2!", font=("Orbitron", 32, "bold"), fill="black", tags="tag_bonus")
            canvas_destino.create_text(x, y, text="🎁 ¡BONUS x2!", font=("Orbitron", 32, "bold"), fill=colores[paso], tags="tag_bonus")
            self.ventana_pregunta.after(200, lambda: actualizar_color((paso + 1) % len(colores)))
        actualizar_color()    

    def actualizar_timer(self):
        if not self.timer_activo: return
        tiempo_pasado = time.time() - self.inicio_timer
        restante = max(0, self.tiempo_total - tiempo_pasado)
        progreso = restante / self.tiempo_total
        segundos = int(restante)
        
        ancho_max, color = 800, "#2DCE05"
        if segundos <= 10:
            color = "#FF3B3B"
            if 9.9 < restante < 10.1:
                self.audio.play("warning")

        self.canvas_pregunta_fondo.delete("timer_texto")
        x, y = self.root.winfo_screenwidth() // 2, 40
        self.canvas_pregunta_fondo.create_text(x, y, text=str(segundos), font=("Orbitron", 35, "bold"), fill=color, tags="timer_texto")

        if hasattr(self, 'barra_progresiva'): self.canvas_pregunta_fondo.delete("barra_dinamica")
        self.barra_progresiva = crear_rectangulo_redondeado(self.canvas_pregunta_fondo, self.x_barra_inicio, self.y_barra_top, self.x_barra_inicio + (ancho_max * progreso), self.y_barra_top + 8, radio=4, fill=color, outline="#003300", width=2, tags="barra_dinamica")

        #self.tiempo_restante = segundos
        if restante <= 0:
            self.timer_activo = False
            pygame.mixer.stop()
            self.audio.play("timeout")
            self.question_manager.marcar_respondida(self.categoria_actual, self.valor_actual)
            
            jugador = self.game_manager.jugador_actual()
            if jugador:
                # 1. Restamos los puntos en el score_manager
                self.score_manager.actualizar_puntos(jugador, -self.puntos_actuales)
                
                # 2. Obtenemos el total real desde la lógica
                puntos_actuales = self.score_manager.obtener_puntaje(jugador)
                
                # 3. Limpiamos el nombre para que coincida con el TAG del Canvas
                # Esto convierte "Eduardo Jose" en "puntos_Eduardo_Jose"
                tag_seguro = f"puntos_{jugador.replace(' ', '_')}"
                
                # 4. Actualizamos visualmente
                self.labels_puntajes[jugador].itemconfig(tag_seguro, text=str(puntos_actuales))
            
            self.finalizar_pregunta()
            
        elif self.timer_activo:
            self.timer_id = self.root.after(100, self.actualizar_timer)

    def cancelar_timers(self):
        try:
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
        except:
            pass

    def verificar_respuesta(self, respuesta):
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        self.timer_activo = False
        
        # 1. Obtener jugador y validar respuesta
        jugador = self.game_manager.jugador_actual()
        es_correcta = respuesta.lower() == self.respuesta_actual.lower()
        
        if es_correcta:
            self.score_manager.responder_correcto(jugador, self.puntos_actuales)
            self.audio.play("correcto")
            color, titulo = "#1FEC75", "¡CORRECTO!"
        else:
            self.score_manager.responder_incorrecto(jugador, self.puntos_actuales)
            self.audio.play("incorrecto")
            color, titulo = "#FF3B3B", "LA RESPUESTA ERA:"

        # 2. Limpiar elementos de la ventana de pregunta
        for w in self.ventana_pregunta.winfo_children():
            if w != self.canvas_pregunta_fondo: 
                w.destroy()

        # 3. Crear el cuadro de revelación de respuesta
        ancho_p = self.root.winfo_screenwidth()
        alto_p = self.root.winfo_screenheight()
        
        canvas_revela = tk.Canvas(self.ventana_pregunta, width=ancho_p * 0.8, height=300, 
                                  bg="#000000", highlightthickness=0)
        canvas_revela.place(relx=0.5, rely=0.6, anchor="center")

        crear_rectangulo_redondeado(canvas_revela, 0, 0, ancho_p * 0.8, 300, radio=30, fill="", outline=color, width=5)
        crear_rectangulo_redondeado(canvas_revela, 5, 5, (ancho_p * 0.8)-5, 295, radio=30, fill="#051205", outline="", width=0)
        
        canvas_revela.create_text(ancho_p * 0.4, 60, text=titulo, 
                                  font=("Orbitron", 24, "bold"), fill="white")
        canvas_revela.create_text(ancho_p * 0.4, 170, text=self.respuesta_actual.upper(), 
                                  font=("Orbitron", 45, "bold"), fill=color, width=ancho_p * 0.7)
        
        # 4. ACTUALIZACIÓN LÓGICA Y VISUAL (CORREGIDA)
        self.casillas_usadas.add((self.categoria_actual, self.valor_actual))
        
        if jugador in self.labels_puntajes:
            # Obtenemos el nuevo puntaje
            nuevo_score = self.score_manager.obtener_puntaje(jugador)
            # USAMOS itemconfig para actualizar el texto dentro del Canvas del jugador
            tag_a_buscar = f"puntos_{jugador.replace(' ', '_')}"
            self.labels_puntajes[jugador].itemconfig(tag_a_buscar, text=str(nuevo_score))

        # 5. Verificación de final de juego
        if len(self.casillas_usadas) >= 42:
            print("--- TABLERO COMPLETADO ---")

        # 6. Esperar y cerrar (Ahora sí llegará aquí sin errores)
        self.ventana_pregunta.after(self.tiempo_revelacion, self.finalizar_pregunta)

    def finalizar_pregunta(self):
        if self.timer_id:
            try:
                self.root.after_cancel(self.timer_id)
            except:
                pass
            self.timer_id = None

       
        # Creamos una clave única para la casilla (Categoría, Valor)
        id_casilla = (self.categoria_actual, self.valor_actual)
        if id_casilla not in self.casillas_usadas:
            self.casillas_usadas.add(id_casilla) # O .add() si es un set
        # -----------------------------------------------------------------

        self.ventana_pregunta.destroy()
        self.reproducir_musica_fondo()

        target = self.botones_tablero.get(id_casilla)
        if target:
            canvas = target["canvas"]
            img_tk = self.imagenes_cache.get(id_casilla)

            if not img_tk:
                fragmento = target["imagen"]
                w, h = canvas.winfo_width(), canvas.winfo_height()
                img_tk = ImageTk.PhotoImage(
                    fragmento.resize((w, h), Image.Resampling.LANCZOS)
                )
                self.imagenes_cache[id_casilla] = img_tk # Guardar en caché para evitar parpadeos
                
            canvas.image_ref = img_tk
            canvas.delete("all")
            canvas.create_image(0, 0, anchor="nw", image=img_tk)
        
        pygame.mixer.music.unpause()
        self.seleccionar_jugador()
        
        total_casillas = len(self.botones_tablero)
        total_usadas = len(self.casillas_usadas) 
        
        print(f"DEBUG TABLERO: {total_usadas} de {total_casillas} completadas.")

        if total_usadas >= total_casillas and total_casillas > 0:
            print("¡Tablero completo! Lanzando ventana ganador...")
            # Aumentamos un poco el delay para que el usuario vea la última imagen en el tablero
            self.root.after(3000, self.mostrar_ganador)

    def mostrar_ganador(self):
        try: pygame.mixer.music.stop(); pygame.mixer.stop()
        except: pass
        self.audio.play("victoria", loops=-1)
        self.ventana_final = tk.Toplevel(self.root)
        self.ventana_final.attributes("-fullscreen", True)
        ancho_p, alto_p = self.root.winfo_screenwidth(), self.root.winfo_screenheight()

        self.canvas_final = tk.Canvas(self.ventana_final, width=ancho_p, height=alto_p, highlightthickness=0)
        self.canvas_final.place(relx=0, rely=0, relwidth=1, relheight=1)

        # --- IMAGEN BLINDADA: PANTALLA GANADOR ---
        try:
            img_path = obtener_ruta_recurso("imagenes", "mesi.png")
            img_fondo = Image.open(img_path).resize((ancho_p, alto_p), Image.LANCZOS)
            self.bg_final_tk = ImageTk.PhotoImage(img_fondo)
            self.canvas_final.create_image(0, 0, image=self.bg_final_tk, anchor="nw")
        except Exception as e:
            print(f"Error cargando imagen final: {e}")
            self.canvas_final.config(bg="#000a00")
            
        confetis = []
        for _ in range(300):
            x, y, size = random.randint(0, ancho_p), random.randint(-600, 0), random.randint(6, 12)
            c = self.canvas_final.create_oval(x, y, x + size, y + size, fill=random.choice(["#FFD700", "#917D0C", "#F5D20C", "#EEEC6D"]), outline="")
            confetis.append((c, random.randint(2, 5), random.choice([-2, -1, 1, 2])))

        def animar():
            for c, vy, vx in confetis:
                self.canvas_final.move(c, vx, vy)
                if self.canvas_final.coords(c)[1] > alto_p: self.canvas_final.move(c, 0, -alto_p - 100)
            if self.ventana_final.winfo_exists(): self.ventana_final.after(40, animar)
        animar()

        dibujar_interfaz_ganador(self.canvas_final, self.score_manager.obtener_todos(), ancho_p, alto_p)

        self.img_btn_re_tk = crear_boton_redondeado("Jugar nuevamente", 320, 80, "#1a4a2a", "#00FF99")
        self.img_btn_fi_tk = crear_boton_redondeado("Finalizar", 320, 80, "#6a1a1a", "#FF3333")
        self.canvas_final.tag_bind(self.canvas_final.create_image(ancho_p//2 - 200, alto_p*0.88, image=self.img_btn_re_tk), "<Button-1>", lambda e: self.reiniciar_juego())
        self.canvas_final.tag_bind(self.canvas_final.create_image(ancho_p//2 + 200, alto_p*0.88, image=self.img_btn_fi_tk), "<Button-1>", lambda e: self.cerrar_juego())



    def reiniciar_juego(self):
        # 1. Limpieza
        if hasattr(self, "ventana_final") and self.ventana_final.winfo_exists():
            self.ventana_final.destroy()
        
        pygame.mixer.stop()
        pygame.mixer.music.stop()

        # 2. Reset de Memoria y Lógica
        self.casillas_usadas = set()
        self.question_manager.reiniciar_preguntas()
        
        # 3. Regenerar Bonus (Configuración dinámica)
        todas_las_casillas_reales = []
        for cat in self.categorias:
            for val in self.valores:
                todas_las_casillas_reales.append((cat, val))
        
        self.bonus_x2 = set(random.sample(todas_las_casillas_reales, 
                            min(self.cantidad_bonus, len(todas_las_casillas_reales))))

        # 4. Resetear Puntajes Visuales (Canvas)
        for j in self.score_manager.puntajes:
            self.score_manager.puntajes[j] = 0
            if j in self.labels_puntajes:
                # Actualizar el número y el color neón a dorado
                tag_seguro = f"puntos_{j.replace(' ', '_')}"
                self.labels_puntajes[j].itemconfig(tag_seguro, text="0", fill="#FFD700")
                self.labels_puntajes[j].itemconfig("marco", outline="#FFD700", width=3)

        # 5. Reconstruir la Interfaz de un solo golpe
        if hasattr(self, "tablero"):
            self.tablero.destroy()
            
        self.crear_tablero() # Solo una vez aquí
        self.reproducir_musica_fondo() # Solo una vez aquí
        
        print(f"--- REINICIO COMPLETADO: Tablero de {len(self.valores)} filas listo ---")