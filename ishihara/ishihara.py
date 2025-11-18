# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random

class IshiharaTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test de Agudeza Visual")
        
        # --- Configuración de la ventana ---
        self.root.minsize(1024, 580)
        self.root.state('zoomed')
        self.root.configure(bg="#1a1a2e")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # --- Paleta de Colores Moderna y Atractiva ---
        self.BG_COLOR = '#1a1a2e'
        self.FRAME_COLOR = '#16213e'
        self.ACCENT_COLOR_1 = '#58a6ff'
        self.ACCENT_COLOR_2 = '#ff6ec7'
        self.BUTTON_COLOR = '#4a235a'
        self.BUTTON_HOVER_COLOR = '#7307A5'
        self.TEXT_COLOR = '#c9d1d9'
        self.ERROR_COLOR = '#e74c3c'
        self.SUCCESS_COLOR = '#4CAF50'
        # MODIFICADO: Color más claro para la pantalla final
        self.RESULTS_BG_COLOR = '#f0f0f0'
        self.RESULTS_TEXT_COLOR = '#333333'
        
        self.root.configure(bg=self.BG_COLOR)

        # --- Variables para el juego ---
        self.aciertos = 0
        self.errores = 0
        self.game_over = False
        self.time_left = 20  # MODIFICADO: Tiempo cambiado a 20 segundos
        self.timer_job = None
        self.imagen_actual = 0
        self.tiempo_limite = 20 # MODIFICADO: Tiempo cambiado a 20 segundos
        self.imagenes_erroneas = []  # NUEVA: Lista para guardar los nombres de las imágenes con error y la respuesta del usuario
        
        # --- Configuración de fuentes ---
        self.title_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=14)
        self.button_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.result_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.timer_font = font.Font(family="Helvetica", size=16, weight="bold")
        
        # --- MODIFICADO: Lista de imágenes locales con sus respuestas ---
        # Se extrajeron las respuestas de las descripciones proporcionadas.
        # "mancha" para patrones sin número, y el número si se especifica.
        self.imagenes = [
            # --- Imágenes originales ---
            {"filename": "1.jpg", "respuesta": "1", "nombre": "1.jpg"},
            {"filename": "2.jpg", "respuesta": "2", "nombre": "2.jpg"},
            {"filename": "2rp.jpg", "respuesta": "2", "nombre": "2rp.jpg"},
            {"filename": "3.jpg", "respuesta": "3", "nombre": "3.jpg"},
            {"filename": "3rp.jpg", "respuesta": "3", "nombre": "3rp.jpg"},
            {"filename": "4.jpg", "respuesta": "4", "nombre": "4.jpg"},
            {"filename": "5.jpg", "respuesta": "5", "nombre": "5.jpg"},
            {"filename": "6.jpg", "respuesta": "6", "nombre": "6.jpg"},
            
            # --- NUEVAS IMÁGENES AÑADIDAS ---
            {"filename": "7.jpg", "respuesta": "7", "nombre": "7.jpg"},
            {"filename": "8.jpg", "respuesta": "8", "nombre": "8.jpg"},
            {"filename": "8rp.jpg", "respuesta": "8", "nombre": "8rp.jpg"},
            {"filename": "9.jpg", "respuesta": "9", "nombre": "9.jpg"},
            {"filename": "12.jpg", "respuesta": "12", "nombre": "12.jpg"},
            {"filename": "16.jpg", "respuesta": "16", "nombre": "16.jpg"},
            {"filename": "29.jpg", "respuesta": "29", "nombre": "29.jpg"},
            {"filename": "42.jpg", "respuesta": "42", "nombre": "42.jpg"},
            
            # --- IMÁGENES DE LA DOCUMENTACIÓN AÑADIDAS ---
            {"filename": "45.jpg", "respuesta": "45", "nombre": "45.jpg"},
            {"filename": "74.jpg", "respuesta": "74", "nombre": "74.jpg"},
            {"filename": "97.jpg", "respuesta": "97", "nombre": "97.jpg"},  # Se menciona "2" o "5"
            {"filename": "mancha.jpg", "respuesta": "mancha", "nombre": "mancha.jpg"},
            {"filename": "mancha2.jpg", "respuesta": "mancha", "nombre": "mancha2.jpg"},
            {"filename": "mancha3.jpg", "respuesta": "mancha", "nombre": "mancha3.jpg"},
            {"filename": "mancha4.jpg", "respuesta": "mancha", "nombre": "mancha4.jpg"},
        ]
        
        random.shuffle(self.imagenes)
        self.imagenes_cargadas = []
        self.cargar_imagenes() # MODIFICADO: Se llama a la nueva función de carga
        self.crear_menu_inicio()

    def crear_menu_inicio(self):
        """Crea la pantalla de bienvenida con un diseño moderno."""
        self.menu_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        # Título principal
        title_label = tk.Label(
            self.menu_frame,
            text="Bienvenido al Test de Ishihara",
            font=self.title_font,
            fg=self.ACCENT_COLOR_1,
            bg=self.BG_COLOR
        )
        title_label.pack(pady=(50, 10))

        # Subtítulo con animación de color
        subtitle_label = tk.Label(
            self.menu_frame,
            text="Prepárate tus sentidos para una prueba de agudeza visual.",
            font=self.normal_font,
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR
        )
        subtitle_label.pack(pady=10)
        
        # Marco para el botón
        button_frame = tk.Frame(self.menu_frame, bg=self.BG_COLOR)
        button_frame.pack(pady=40)

        # Botón de inicio con efecto hover
        self.start_button = tk.Button(
            button_frame,
            text="Empecemos",
            command=self.iniciar_juego,
            font=self.button_font,
            bg=self.BUTTON_COLOR,
            fg=self.TEXT_COLOR,
            relief=tk.FLAT,
            padx=40,
            pady=15,
            cursor="hand2",
            activebackground=self.BUTTON_HOVER_COLOR,
            borderwidth=0
        )
        self.start_button.pack()

        # --- Efecto de animación de texto ---
        self.animate_text_color(subtitle_label, self.TEXT_COLOR, self.ACCENT_COLOR_1, 2000)

    def animate_text_color(self, widget, color1, color2, duration_ms):
        """Cambia gradualmente el color de un widget de un color a otro."""
        widget.config(fg=color1)
        self.root.after(duration_ms, lambda: widget.config(fg=color2))

    def iniciar_juego(self):
        """Oculta el menú y muestra la interfaz del juego."""
        self.menu_frame.pack_forget()
        
        # --- CORRECCIÓN: Se crean los widgets solo una vez ---
        if not hasattr(self, 'game_frame'):
            self.crear_widgets_juego()
        
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        self.frame_info.pack(fill=tk.X, pady=(10, 0))
        self.frame_contenido.pack(fill=tk.BOTH, expand=True)
        self.canvas_imagen.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.frame_interaccion.pack(fill=tk.X, pady=(0, 20))
        self.label_resultado.pack(fill=tk.X, pady=(0, 20))

        self.reset_game_state()
        self.mostrar_imagen()

    def crear_widgets_juego(self):
        """Crea todos los widgets necesarios para el juego."""
        self.game_frame = tk.Frame(self.root, bg=self.FRAME_COLOR)
        
        self.frame_info = tk.Frame(self.game_frame, bg="white", relief=tk.RAISED, borderwidth=1)
        self.frame_info.pack(fill=tk.X, pady=(10, 0))
        
        self.label_temporizador = tk.Label(self.frame_info, text=f"Tiempo: {self.tiempo_limite}s", font=self.timer_font, bg="white", fg=self.TEXT_COLOR)
        self.label_temporizador.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.label_aciertos = tk.Label(self.frame_info, text=f"Aciertos: {self.aciertos}", font=self.normal_font, bg="white", fg=self.SUCCESS_COLOR)
        self.label_aciertos.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.label_errores = tk.Label(self.frame_info, text=f"Errores: {self.errores}", font=self.normal_font, bg="white", fg=self.ERROR_COLOR)
        self.label_errores.pack(side=tk.LEFT, padx=20, pady=10)

        self.label_progreso = tk.Label(self.frame_info, text=f"Imagen {self.imagen_actual + 1} de {len(self.imagenes_cargadas)}", font=self.normal_font, bg="white", fg=self.TEXT_COLOR)
        self.label_progreso.pack(side=tk.RIGHT, padx=20, pady=10)

        self.frame_contenido = tk.Frame(self.game_frame, bg="white", relief=tk.RAISED, borderwidth=2)
        self.frame_contenido.rowconfigure(0, weight=1)
        self.frame_contenido.columnconfigure(0, weight=1)
        
        self.canvas_imagen = tk.Canvas(self.frame_contenido, bg="white", highlightthickness=0)
        self.canvas_imagen.bind('<Configure>', self.on_canvas_resize)

        self.frame_interaccion = tk.Frame(self.frame_contenido, bg="white")
        self.frame_interaccion.pack(fill=tk.X, pady=(0, 20))
        
        # MODIFICADO: Texto de la pregunta actualizado
        self.label_pregunta = tk.Label(self.frame_interaccion, text="¿Qué ves en la imagen? (Número, 'lineas' o 'mancha')", font=self.normal_font, bg="white")
        self.label_pregunta.pack(pady=5)
        
        self.entry_respuesta = tk.Entry(self.frame_interaccion, font=self.normal_font, width=15, justify='center', relief=tk.FLAT, borderwidth=2, bg="#F5F5F5")
        self.entry_respuesta.pack(pady=5)
        self.entry_respuesta.bind("<KeyRelease>", self.verificar_entrada)
        self.entry_respuesta.bind("<Return>", lambda event: self.verificar_respuesta())
        
        self.boton_verificar = tk.Button(self.frame_interaccion, text="Verificar", command=self.verificar_respuesta, font=self.button_font, bg=self.BUTTON_COLOR, fg=self.TEXT_COLOR, relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        self.boton_verificar.pack(pady=10)

        self.label_resultado = tk.Label(self.frame_contenido, text="", font=self.result_font, bg="white", height=2)
        self.label_resultado.pack(fill=tk.X, pady=(0, 20))

    def reset_game_state(self):
        """Reinicia las variables del juego a su estado inicial y actualiza las etiquetas."""
        self.aciertos = 0
        self.errores = 0
        self.imagen_actual = 0
        self.game_over = False
        self.time_left = self.tiempo_limite
        self.imagenes_erroneas = [] # MODIFICACIÓN: Limpiar la lista de errores
        
        self.label_aciertos.config(text=f"Aciertos: {self.aciertos}")
        self.label_errores.config(text=f"Errores: {self.errores}")
        self.label_resultado.config(text="")

    # MODIFICADO: Función renombrada y lógica cambiada para carga local
    def cargar_imagenes(self):
        """Carga las imágenes desde archivos locales en lugar de descargarlas."""
        for img_data in self.imagenes:
            try:
                # Intenta abrir la imagen desde el archivo local
                img = Image.open(img_data["filename"])
                self.imagenes_cargadas.append({
                    "pil_image": img,
                    "respuesta": img_data["respuesta"],
                    "nombre": img_data["nombre"]
                })
            except FileNotFoundError:
                print(f"Error: No se encontró el archivo {img_data['nombre']}. Creando imagen de respaldo.")
                self.imagenes_cargadas.append(self.crear_imagen_respaldo(img_data))
            except Exception as e:
                print(f"Error al cargar {img_data['nombre']}: {e}. Creando imagen de respaldo.")
                self.imagenes_cargadas.append(self.crear_imagen_respaldo(img_data))

    def crear_imagen_respaldo(self, img_data):
        """Crea una imagen de respaldo si el archivo local no se encuentra o falla."""
        respuesta = img_data["respuesta"]
        img = Image.new('RGB', (400, 400), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 80)
        except IOError:
            font = ImageFont.load_default()
        
        text_color = '#333333'
        # Muestra la respuesta correcta en la imagen de respaldo
        draw.text((200, 180), f"Archivo no encontrado\nRespuesta: {respuesta}", font=font, fill=text_color, anchor="mm")
        
        return {
            "pil_image": img,
            "respuesta": respuesta,
            "nombre": img_data["nombre"]
        }

    def on_canvas_resize(self, event):
        if self.game_over:
            return
        if self.imagen_actual < len(self.imagenes_cargadas):
            self.mostrar_imagen_en_canvas(event.width, event.height)

    def mostrar_imagen_en_canvas(self, canvas_width, canvas_height):
        pil_img = self.imagenes_cargadas[self.imagen_actual]["pil_image"]
        
        img_ratio = pil_img.width / pil_img.height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            new_width = canvas_width - 40
            new_height = int(new_width / img_ratio)
        else:
            new_height = canvas_height - 40
            new_width = int(new_height * img_ratio)
        
        resized_img = pil_img.resize((new_width, new_height), Image.LANCZOS)
        self.current_photo = ImageTk.PhotoImage(resized_img)

        self.canvas_imagen.delete("all")
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.canvas_imagen.create_image(x, y, anchor="nw", image=self.current_photo)

    def mostrar_imagen(self):
        if self.game_over:
            return
            
        self.game_over = False
        
        if self.imagen_actual < len(self.imagenes_cargadas):
            self.canvas_imagen.update_idletasks()
            self.mostrar_imagen_en_canvas(self.canvas_imagen.winfo_width(), self.canvas_imagen.winfo_height())
            
            self.entry_respuesta.delete(0, tk.END)
            self.entry_respuesta.focus()
            
            self.label_resultado.config(text="")
            self.label_progreso.config(text=f"Imagen {self.imagen_actual + 1} de {len(self.imagenes_cargadas)}")
            
            self.iniciar_temporizador()
        else:
            self.mostrar_resultado_final()

    def iniciar_temporizador(self):
        self.time_left = self.tiempo_limite
        self.actualizar_label_temporizador()
        
        self.entry_respuesta.config(state=tk.NORMAL)
        self.boton_verificar.config(state=tk.DISABLED)

        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        
        self.contar_hacia_atras()

    def contar_hacia_atras(self):
        if self.time_left > 0 and not self.game_over:
            self.time_left -= 1
            self.actualizar_label_temporizador()
            self.timer_job = self.root.after(1000, self.contar_hacia_atras)
        else:
            self.tiempo_agotado()

    def actualizar_label_temporizador(self):
        color = self.TEXT_COLOR
        if self.time_left <= 5:
            color = self.ERROR_COLOR
        self.label_temporizador.config(text=f"Tiempo: {self.time_left}s", fg=color)

    def verificar_entrada(self, event):
        if self.entry_respuesta.get().strip():
            self.boton_verificar.config(state=tk.NORMAL)
        else:
            self.boton_verificar.config(state=tk.DISABLED)

    def verificar_respuesta(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        respuesta_usuario = self.entry_respuesta.get().strip()
        respuesta_correcta = self.imagenes_cargadas[self.imagen_actual]["respuesta"]
        
        self.entry_respuesta.delete(0, tk.END)
        self.entry_respuesta.config(state=tk.DISABLED)
        self.boton_verificar.config(state=tk.DISABLED)
        
        if self.es_respuesta_valida(respuesta_usuario, respuesta_correcta):
            self.aciertos += 1
            self.label_aciertos.config(text=f"Aciertos: {self.aciertos}")
            self.label_resultado.config(text="✓ Correcto", fg=self.SUCCESS_COLOR)
            self.animate_text_color(self.label_resultado, self.SUCCESS_COLOR, self.TEXT_COLOR, 500)
        else:
            self.errores += 1
            self.label_errores.config(text=f"Errores: {self.errores}")
            self.label_resultado.config(text=f"✗ Incorrecto. La respuesta correcta era: {respuesta_correcta}", fg=self.ERROR_COLOR)
            self.animate_text_color(self.label_resultado, self.ERROR_COLOR, self.TEXT_COLOR, 500)
            # MODIFICACIÓN: Guardar la imagen con error y la respuesta del usuario
            self.imagenes_erroneas.append({
                "nombre": self.imagenes_cargadas[self.imagen_actual]["nombre"],
                "respuesta_usuario": respuesta_usuario,
                "respuesta_correcta": respuesta_correcta
            })
        
        self.root.after(1500, self.siguiente_imagen)

    # MODIFICADO: Lógica de validación actualizada para "mancha"
    def es_respuesta_valida(self, usuario, correcta):
        """Verifica si la respuesta del usuario es válida, aceptando 'linea'/'lineas' y 'mancha'."""
        if correcta.lower() == "lineas":
            return usuario.lower() in ["linea", "lineas"]
        if correcta.lower() == "mancha": # Nueva regla para "mancha"
            return usuario.lower() == "mancha"
        return usuario.lower() == correcta.lower()

    def tiempo_agotado(self):
        self.entry_respuesta.delete(0, tk.END)
        self.errores += 1
        self.label_errores.config(text=f"Errores: {self.errores}")
        self.label_resultado.config(text=f"¡Tiempo agotado! La respuesta correcta era: {self.imagenes_cargadas[self.imagen_actual]['respuesta']}", fg=self.ERROR_COLOR)
        self.animate_text_color(self.label_resultado, self.ERROR_COLOR, self.TEXT_COLOR, 500)
        # MODIFICACIÓN: Guardar la imagen con error y la respuesta del usuario (vacía en este caso)
        self.imagenes_erroneas.append({
            "nombre": self.imagenes_cargadas[self.imagen_actual]["nombre"],
            "respuesta_usuario": "(sin respuesta)",
            "respuesta_correcta": self.imagenes_cargadas[self.imagen_actual]["respuesta"]
        })
        
        self.root.after(1500, self.siguiente_imagen)
    
    def siguiente_imagen(self):
        self.imagen_actual += 1
        self.mostrar_imagen()
    
    def mostrar_resultado_final(self):
        self.game_over = True
        
        if self.timer_job:
            self.root.after_cancel(self.timer_job)

        self.frame_contenido.pack_forget()
        self.frame_interaccion.pack_forget()
        self.label_resultado.pack_forget()

        # MODIFICADO: Usar un color más claro para la pantalla de resultados
        self.frame_resultado_final = tk.Frame(self.root, bg=self.RESULTS_BG_COLOR)
        self.frame_resultado_final.pack(fill=tk.BOTH, expand=True)

        # MODIFICACIÓN: Cambiar el texto de resultados para mostrar la respuesta del usuario
        resultado_texto = "Test completado\n\n"
        resultado_texto += f"Aciertos: {self.aciertos}\n"
        resultado_texto += f"Errores: {self.errores}\n\n"
        
        if self.imagenes_erroneas:
            resultado_texto += "Imágenes con respuesta incorrecta:\n"
            for error in self.imagenes_erroneas:
                resultado_texto += f"{error['nombre']}: Tú respondiste '{error['respuesta_usuario']}' (Correcto: {error['respuesta_correcta']})\n"
        else:
            resultado_texto += "¡No cometiste ningún error!"
        
        # MODIFICADO: Usar colores más claros para el texto de resultados
        self.label_resultado_final = tk.Label(
            self.frame_resultado_final, 
            text=resultado_texto, 
            font=self.result_font, 
            bg=self.RESULTS_BG_COLOR, 
            fg=self.RESULTS_TEXT_COLOR,
            justify=tk.LEFT
        )
        self.label_resultado_final.pack(pady=20, expand=True)
        
        self.frame_botones_finales = tk.Frame(self.frame_resultado_final, bg=self.RESULTS_BG_COLOR)
        self.frame_botones_finales.pack(pady=10)
        
        menu_button = tk.Button(
            self.frame_botones_finales, 
            text="Volver al Menú", 
            command=self.mostrar_menu_inicio, 
            font=self.button_font, 
            bg=self.ACCENT_COLOR_1, 
            fg="white",  # MODIFICADO: Cambiado a blanco para mejor contraste
            relief=tk.FLAT, 
            padx=20, 
            pady=8, 
            cursor="hand2"
        )
        menu_button.pack(side=tk.LEFT, padx=10)
        
        close_button = tk.Button(
            self.frame_botones_finales, 
            text="Cerrar", 
            command=self.root.quit, 
            font=self.button_font, 
            bg=self.ERROR_COLOR, 
            fg="white", 
            relief=tk.FLAT, 
            padx=20, 
            pady=8, 
            cursor="hand2"
        )
        close_button.pack(side=tk.LEFT, padx=10)
    
    def mostrar_menu_inicio(self):
        # --- CORRECCIÓN: Se verifica si el widget existe antes de intentar ocultarlo ---
        if hasattr(self, 'game_frame'):
            self.game_frame.pack_forget()
        if hasattr(self, 'frame_resultado_final'):
            self.frame_resultado_final.pack_forget()

        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        
        self.reset_game_state()

# --- Ejecución del Programa ---
if __name__ == "__main__":
    root = tk.Tk()
    app = IshiharaTestApp(root)
    root.mainloop()