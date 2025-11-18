import tkinter as tk
from tkinter import font, messagebox
import random
import smtplib
import os
from email.message import EmailMessage
from email.mime.image import MIMEImage

try:
    from PIL import Image, ImageGrab, UnidentifiedImageError, ImageTk
except ImportError:
    print("Error: La librería Pillow no está instalada.")
    print("Por favor, instálala con: pip install Pillow")
    exit()

class AgilidadVisualApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Configuración de la Ventana Principal ---
        self.title("Test de Agilidad Visual")
        self.geometry("800x600")
        self.config(bg="#2c3e50")

        # --- Variables del Juego ---
        self.aciertos = 0
        self.fallos = 0
        self.no_presionado = 0
        self.puntos_rojos_generados = 0
        self.total_puntos_rojos = 40
        
        self.punto_rojo_actual = None
        self.punto_rojo_activo = False
        self.punto_rojo_ya_acertado = False

        # Lista para guardar el historial de puntos con coordenadas relativas
        self.historial_puntos = []
        
        # Variable para almacenar la ruta de la imagen del mapa
        self.mapa_imagen_path = None

        # --- Iniciar la primera pantalla ---
        self.crear_pantalla_inicio()

    def limpiar_ventana(self):
        """Destruye todos los widgets en la ventana actual."""
        for widget in self.winfo_children():
            widget.destroy()

    def crear_pantalla_inicio(self):
        """Crea y muestra la pantalla de bienvenida."""
        self.limpiar_ventana()

        frame_card = tk.Frame(self, bg="#ecf0f1", relief="solid", bd=1, padx=50, pady=40)
        frame_card.pack(expand=True, pady=50)

        fuente_titulo = font.Font(family="Arial", size=28, weight="bold")
        titulo_label = tk.Label(
            frame_card,
            text="Test de Agilidad Visual",
            font=fuente_titulo,
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        titulo_label.pack(pady=(0, 20))

        fuente_instrucciones = font.Font(family="Arial", size=13)
        instrucciones_texto = (
            "¿Rápido para reaccionar?\n\n"
            "1. Aparecerán puntos rojos al azar en la pantalla.\n"
            "2. Presiona la BARRA ESPACIADORA tan pronto veas un punto rojo.\n"
            "   ¡Importante! Presiona solo UNA VEZ por punto.\n"
            "3. ¡No presiones si no hay nada!\n\n"
            "El test se vuelve más difícil a medida que avanzas.\n"
            "¡Mucha suerte!"
        )
        instrucciones_label = tk.Label(
            frame_card,
            text=instrucciones_texto,
            font=fuente_instrucciones,
            bg="#ecf0f1",
            fg="#34495e",
            justify="center"
        )
        instrucciones_label.pack(pady=10)

        fuente_boton = font.Font(family="Arial", size=16, weight="bold")
        boton_iniciar = tk.Button(
            frame_card,
            text="Iniciar Test",
            font=fuente_boton,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            padx=30,
            pady=12,
            relief="flat",
            command=self.iniciar_juego,
            cursor="hand2"
        )
        boton_iniciar.pack(pady=(30, 0))

    def iniciar_juego(self):
        """Prepara y comienza la partida."""
        self.limpiar_ventana()
        
        # Resetear variables del juego
        self.aciertos = 0
        self.fallos = 0
        self.no_presionado = 0
        self.puntos_rojos_generados = 0
        self.historial_puntos = []
        self.punto_rojo_activo = False
        self.punto_rojo_ya_acertado = False
        self.mapa_imagen_path = None

        # --- Crear la interfaz del juego ---
        frame_marcador = tk.Frame(self, bg="#34495e", pady=10)
        frame_marcador.pack(fill="x")
        
        fuente_marcador = font.Font(family="Arial", size=14, weight="bold")
        self.label_aciertos = tk.Label(frame_marcador, text=f"Aciertos: {self.aciertos}", font=fuente_marcador, bg="#34495e", fg="#2ecc71")
        self.label_aciertos.pack(side="left", padx=40)
        
        self.label_fallos = tk.Label(frame_marcador, text=f"Fallos: {self.fallos}", font=fuente_marcador, bg="#34495e", fg="#e74c3c")
        self.label_fallos.pack(side="left", padx=40)

        self.label_no_presionado = tk.Label(frame_marcador, text=f"No presionado: {self.no_presionado}", font=fuente_marcador, bg="#34495e", fg="#f1c40f")
        self.label_no_presionado.pack(side="left", padx=40)
        
        self.canvas_juego = tk.Canvas(self, bg="#ecf0f1", highlightthickness=0)
        self.canvas_juego.pack(fill="both", expand=True, padx=20, pady=20)

        self.dibujar_punto_negro()
        
        self.bind("<space>", self.manejar_espacio)

        self.after(1500, self.programar_siguiente_punto_rojo)

    def dibujar_punto_negro(self):
        """Dibuja el punto negro en el centro del canvas."""
        self.canvas_juego.update_idletasks()
        canvas_width = self.canvas_juego.winfo_width()
        canvas_height = self.canvas_juego.winfo_height()
        self.canvas_juego.delete("punto_negro")
        
        radio = 10
        self.canvas_juego.create_oval(
            canvas_width // 2 - radio, canvas_height // 2 - radio,
            canvas_width // 2 + radio, canvas_height // 2 + radio,
            fill="black", tags="punto_negro"
        )
        self.bind("<Configure>", lambda e: self.dibujar_punto_negro())

    def programar_siguiente_punto_rojo(self):
        """Programa la aparición del siguiente punto rojo si el juego no ha terminado."""
        if self.puntos_rojos_generados < self.total_puntos_rojos:
            tiempo_espera = random.randint(2000, 4000)
            self.after(tiempo_espera, self.mostrar_punto_rojo)
        else:
            self.after(2000, self.finalizar_juego)

    def mostrar_punto_rojo(self):
        """Muestra un punto rojo y guarda su posición relativa en el historial."""
        if self.puntos_rojos_generados >= self.total_puntos_rojos:
            return

        self.puntos_rojos_generados += 1
        
        self.canvas_juego.update_idletasks()
        canvas_width = self.canvas_juego.winfo_width()
        canvas_height = self.canvas_juego.winfo_height()

        if self.puntos_rojos_generados >= 15:
            size = 2 
        else:
            size = 4 
        
        x = random.randint(size, canvas_width - size)
        y = random.randint(size, canvas_height - size)

        self.punto_rojo_actual = self.canvas_juego.create_oval(
            x - size, y - size, x + size, y + size,
            fill="#e74c3c", outline="#e74c3c", tags="punto_rojo"
        )
        self.punto_rojo_activo = True
        self.punto_rojo_ya_acertado = False

        rel_x = x / canvas_width
        rel_y = y / canvas_height
        self.historial_puntos.append({'rx': rel_x, 'ry': rel_y, 'presionado': False})

        self.after(600, self.ocultar_punto_rojo)

    def ocultar_punto_rojo(self):
        """Oculta el punto rojo y comprueba si no fue presionado."""
        if self.punto_rojo_actual:
            self.canvas_juego.delete(self.punto_rojo_actual)
            self.punto_rojo_actual = None

        if self.punto_rojo_activo and not self.punto_rojo_ya_acertado:
            self.no_presionado += 1
            self.actualizar_marcador()

        self.punto_rojo_activo = False
        self.programar_siguiente_punto_rojo()

    def manejar_espacio(self, event):
        """Maneja el evento de presionar la barra espaciadora."""
        if self.punto_rojo_activo:
            if not self.punto_rojo_ya_acertado:
                self.aciertos += 1
                if self.historial_puntos:
                    self.historial_puntos[-1]['presionado'] = True
                self.punto_rojo_ya_acertado = True
            else:
                self.fallos += 1
        else:
            self.fallos += 1
        
        self.actualizar_marcador()

    def actualizar_marcador(self):
        """Actualiza las etiquetas del marcador en pantalla."""
        self.label_aciertos.config(text=f"Aciertos: {self.aciertos}")
        self.label_fallos.config(text=f"Fallos: {self.fallos}")
        self.label_no_presionado.config(text=f"No presionado: {self.no_presionado}")

    def _generar_imagen_mapa(self, canvas, filename="mapa_resultados.png"):
        """
        Genera un archivo de imagen PNG haciendo una captura de pantalla del canvas.
        Este método es mucho más robusto y no depende de Ghostscript.
        """
        try:
            # Forzar a que el canvas se dibuje completamente antes de capturar
            canvas.update_idletasks()
            
            # Obtener las coordenadas y dimensiones del canvas en la pantalla
            x = canvas.winfo_rootx()
            y = canvas.winfo_rooty()
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # Definir el área de la captura (bounding box)
            bbox = (x, y, x + width, y + height)
            
            # Capturar la imagen del área definida
            img = ImageGrab.grab(bbox=bbox)
            
            # Guardar la imagen
            img.save(filename, "png")
            
            return filename
        except Exception as e:
            messagebox.showerror("Error de Captura", f"No se pudo capturar la imagen del mapa: {e}")
            return None

    def enviar_resultados_por_email(self):
        """Crea una ventana para enviar los resultados por email."""
        self.limpiar_ventana()
        
        frame_correo = tk.Frame(self, bg="#ecf0f1", relief="solid", bd=1, padx=50, pady=40)
        frame_correo.pack(expand=True, fill="both", pady=50)
        
        fuente_titulo = font.Font(family="Arial", size=20, weight="bold")
        titulo_label = tk.Label(
            frame_correo,
            text="Enviar Resultados por Email",
            font=fuente_titulo,
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        titulo_label.pack(pady=(0, 20))
        
        logo_label = tk.Label(
            frame_correo,
            text="GMAIL",
            font=("Arial", 24, "bold"),
            bg="#ecf0f1",
            fg="#ea4335"
        )
        logo_label.pack(pady=(0, 20))
        
        remitente_label = tk.Label(
            frame_correo,
            text="Mi correo: luisochoa.1495@gmail.com",
            bg="#4285f4",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        )
        remitente_label.pack(pady=5, fill="x")
        
        frame_campos = tk.Frame(frame_correo, bg="#ecf0f1")
        frame_campos.pack(fill="both", expand=True, pady=10)
        
        tk.Label(
            frame_campos,
            text="Destinatario:",
            bg="#ecf0f1",
            fg="black",
            font=("Arial", 10, "bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        self.destinatario_entry = tk.Entry(frame_campos, width=40)
        self.destinatario_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        tk.Label(
            frame_campos,
            text="Asunto:",
            bg="#ecf0f1",
            fg="black",
            font=("Arial", 10, "bold"),
            anchor="w"
        ).grid(row=1, column=0, sticky="w", pady=5)
        
        self.asunto_entry = tk.Entry(frame_campos, width=40)
        self.asunto_entry.insert(0, "Resultados del Test de Agilidad Visual")
        self.asunto_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        tk.Label(
            frame_campos,
            text="Mensaje:",
            bg="#ecf0f1",
            fg="black",
            font=("Arial", 10, "bold"),
            anchor="nw"
        ).grid(row=2, column=0, sticky="nw", pady=5)
        
        self.mensaje_text = tk.Text(frame_campos, height=8, width=40, padx=5, pady=5)
        self.mensaje_text.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        mensaje_predefinido = (
            f"Hola,\n\n"
            f"Aquí están los resultados de tu Test de Agilidad Visual:\n\n"
            f"----------------------------------------\n"
            f"Aciertos: {self.aciertos}\n"
            f"Fallos: {self.fallos}\n"
            f"No presionado: {self.no_presionado}\n"
            f"----------------------------------------\n\n"
            f"¡Gracias por participar!"
        )
        self.mensaje_text.insert("1.0", mensaje_predefinido)
        
        frame_botones = tk.Frame(frame_correo, bg="#ecf0f1")
        frame_botones.pack(pady=20)
        
        fuente_boton = font.Font(family="Arial", size=12, weight="bold")
        
        boton_enviar = tk.Button(
            frame_botones,
            text="ENVIAR",
            font=fuente_boton,
            bg="black",
            fg="white",
            activebackground="#333333",
            padx=20,
            pady=10,
            relief="flat",
            command=self.enviar_email,
            cursor="hand2"
        )
        boton_enviar.pack(side="left", padx=10)
        
        boton_cancelar = tk.Button(
            frame_botones,
            text="CANCELAR",
            font=fuente_boton,
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            padx=20,
            pady=10,
            relief="flat",
            command=self.crear_pantalla_resultados_mapa,
            cursor="hand2"
        )
        boton_cancelar.pack(side="left", padx=10)
    
    def enviar_email(self):
        """Envía el email con los resultados."""
        destinatario = self.destinatario_entry.get()
        asunto = self.asunto_entry.get()
        mensaje = self.mensaje_text.get("1.0", "end-1c")
        
        if not destinatario:
            messagebox.showwarning("Datos Incompletos", "Por favor, ingrese un correo electrónico.")
            return
        
        # --- CONFIGURACIÓN SMTP ---
        remitente = "theo.cattaneo.m@gmail.com" 
        smtp_password = "xqvc saaj xlqc rnpy" 

        # Estructura del email
        email = EmailMessage()
        email["From"] = remitente
        email["To"] = destinatario
        email["Subject"] = asunto
        email.set_content(mensaje)
        
        # Adjuntar la imagen si ya fue generada
        if self.mapa_imagen_path and os.path.exists(self.mapa_imagen_path):
            with open(self.mapa_imagen_path, 'rb') as f:
                img_data = f.read()
            email.add_attachment(img_data, maintype='image', subtype='png', filename=os.path.basename(self.mapa_imagen_path))
        
        # Envío del email
        try:
            smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            smtp.login(remitente, smtp_password)
            smtp.send_message(email)
            messagebox.showinfo("MENSAJERÍA", "Mensaje enviado correctamente")
            smtp.quit()
            
            # Volver a la pantalla de resultados
            self.crear_pantalla_resultados_mapa()
            
        except smtplib.SMTPAuthenticationError:
            error_msg = (
                "Error de autenticación.\n\n"
                "Revisa que el correo y la contraseña de aplicación son correctos.\n"
                "Asegúrate de haber activado la verificación en dos pasos y de usar\n"
                "una 'Contraseña de aplicación' de Google, no tu contraseña habitual."
            )
            messagebox.showerror("Error de Autenticación", error_msg)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo: {e}")

    def crear_pantalla_resultados_mapa(self):
        """Muestra el mapa de resultados con el plano cartesiano y botones."""
        self.limpiar_ventana()
        self.unbind("<space>")
        self.unbind("<Configure>")

        frame_final = tk.Frame(self, bg="#2c3e50")
        frame_final.pack(fill="both", expand=True)

        fuente_titulo = font.Font(family="Arial", size=24, weight="bold")
        titulo = tk.Label(frame_final, text="Mapa de Resultados", font=fuente_titulo, bg="#2c3e50", fg="white")
        titulo.pack(pady=10)

        mapa_ancho = 700
        mapa_alto = 400
        self.canvas_mapa = tk.Canvas(frame_final, width=mapa_ancho, height=mapa_alto, bg="#ecf0f1", highlightthickness=1, highlightbackground="#34495e")
        self.canvas_mapa.pack(pady=10)

        centro_x, centro_y = mapa_ancho / 2, mapa_alto / 2
        self.canvas_mapa.create_line(0, centro_y, mapa_ancho, centro_y, fill="#34495e", width=2, arrow=tk.LAST)
        self.canvas_mapa.create_text(mapa_ancho - 15, centro_y - 15, text="X", font=("Arial", 12, "bold"), fill="#34495e")
        self.canvas_mapa.create_line(centro_x, mapa_alto, centro_x, 0, fill="#34495e", width=2, arrow=tk.LAST)
        self.canvas_mapa.create_text(centro_x + 15, 15, text="Y", font=("Arial", 12, "bold"), fill="#34495e")

        for punto in self.historial_puntos:
            rel_x, rel_y = punto['rx'], punto['ry']
            final_x = rel_x * mapa_ancho
            final_y = rel_y * mapa_alto

            if punto['presionado']:
                self.canvas_mapa.create_oval(final_x-5, final_y-5, final_x+5, final_y+5, fill="#2ecc71", outline="#27ae60")
            else:
                self.canvas_mapa.create_line(final_x-6, final_y-6, final_x+6, final_y+6, fill="#e74c3c", width=3)
                self.canvas_mapa.create_line(final_x-6, final_y+6, final_x+6, final_y-6, fill="#e74c3c", width=3)

        frame_resumen = tk.Frame(frame_final, bg="#2c3e50")
        frame_resumen.pack(pady=10)

        fuente_resumen = font.Font(family="Arial", size=16)
        resumen_texto = f"Aciertos: {self.aciertos}  |  Fallos: {self.fallos}  |  No presionado: {self.no_presionado}"
        tk.Label(frame_resumen, text=resumen_texto, font=fuente_resumen, bg="#2c3e50", fg="white").pack(pady=5)

        frame_botones = tk.Frame(frame_final, bg="#2c3e50")
        frame_botones.pack(pady=10)
        
        fuente_boton = font.Font(family="Arial", size=14, weight="bold")
        
        boton_email = tk.Button(
            frame_botones,
            text="Enviar Resultados por Email",
            font=fuente_boton,
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            padx=20,
            pady=10,
            relief="flat",
            command=self.enviar_resultados_por_email,
            cursor="hand2"
        )
        boton_email.pack(side="left", padx=10)

        boton_volver = tk.Button(
            frame_botones,
            text="Volver al Menú",
            font=fuente_boton,
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            padx=20,
            pady=10,
            relief="flat",
            command=self.crear_pantalla_inicio,
            cursor="hand2"
        )
        boton_volver.pack(side="left", padx=10)
        
        # Generar la imagen del mapa después de que se haya dibujado completamente
        self.after(100, self._generar_y_guardar_mapa)

    def _generar_y_guardar_mapa(self):
        """Genera y guarda la imagen del mapa para usarla posteriormente."""
        self.mapa_imagen_path = self._generar_imagen_mapa(self.canvas_mapa)

    def finalizar_juego(self):
        """Llama a la función que crea la pantalla de resultados con el mapa."""
        self.crear_pantalla_resultados_mapa()


if __name__ == "__main__":
    app = AgilidadVisualApp()
    app.mainloop()