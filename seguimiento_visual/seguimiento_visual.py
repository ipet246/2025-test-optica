import tkinter as tk
import random
import math

class VisualTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trabajo de Seguimiento Visual")
        
        # --- Configuración de la Ventana ---
        self.root.state('zoomed')
        
        # --- NUEVA PALETA DE COLORES MODERNA ---
        self.BG_COLOR = '#0a0e27'          # Azul muy oscuro para el fondo
        self.FRAME_COLOR = '#151932'      # Azul un poco más claro para marcos
        self.TEXT_COLOR = '#e0e0e0'        # Blanco suave para el texto
        self.ACCENT_COLOR = '#00ffff'      # Cian brillante para acentos
        self.BUTTON_COLOR = '#1e90ff'      # Azul "Dodger Blue" para botones
        self.BUTTON_HOVER_COLOR = '#4169e1' # Azul "Royal Blue" para hover

        self.root.configure(bg=self.BG_COLOR)

        # --- Diccionarios de Configuración ---
        # --- MODIFICACIÓN: Tamaños de los círculos ajustados ---
        self.size_map = {
            'Chico': 12,
            'Mediano': 20,
            'Grande': 24       # Ajustado para ser un poco más grande que 'Mediano'
        }
        self.color_map = {
            'Azul': '#4169e1',
            'Verde': '#32cd32',
            'Blanco': '#f0f8ff',
            'Violeta': '#9370db',
            'Rojo': '#dc143c'
        }
        self.movement_map = {
            'Horizontal': 'horizontal',
            'Vertical': 'vertical',
            'Aleatorio': 'random'  # Opción aleatoria añadida
        }

        # --- Variables de Control (se inicializarán con los valores por defecto) ---
        self.flash_size = self.size_map['Mediano']
        self.flash_color = self.color_map['Azul']
        self.movement_mode = self.movement_map['Horizontal']
        
        self.flash_speed = 5
        # Variable para el aumento de velocidad
        self.speed_increase_amount = 0.5
        self.animation_delay_ms = 20
        self.animation_duration = 25
        
        self.is_animating = False
        self.time_left = self.animation_duration
        self.timer_job = None
        self.return_timer = 4
        self.return_timer_job = None
        
        # Variable para mantener la referencia al frame del menú actual
        self.current_menu_frame = None

        # --- Fuente Moderna ---
        try:
            self.default_font = ("Segoe UI", 12)
            self.title_font = ("Segoe UI", 40, "bold")
            self.button_font = ("Segoe UI", 16, "bold")
        except tk.TclError:
            self.default_font = ("Helvetica", 12)
            self.title_font = ("Helvetica", 40, "bold")
            self.button_font = ("Helvetica", 16, "bold")

        self.create_size_menu() # El primer menú es el de tamaño

    def limpiar_menu_actual(self):
        """Destruye el frame del menú actual si existe y si no ha sido destruido ya."""
        # Se añade una comprobación para evitar errores si el widget ya no existe.
        if self.current_menu_frame and self.current_menu_frame.winfo_exists():
            self.current_menu_frame.destroy()

    # --- FUNCIONES DE MENÚ ---
    def create_generic_menu(self, title_text, options_dict, callback_function):
        """Crea un menú genérico basado en un título y un diccionario de opciones."""
        self.limpiar_menu_actual()
        self.current_menu_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.current_menu_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            self.current_menu_frame,
            text=title_text,
            font=self.title_font,
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR
        )
        title_label.pack(pady=(80, 40))

        button_frame = tk.Frame(self.current_menu_frame, bg=self.BG_COLOR)
        button_frame.pack(pady=20)

        for option_name in options_dict.keys():
            btn = tk.Button(
                button_frame,
                text=option_name,
                font=self.button_font,
                bg=self.BUTTON_COLOR,
                fg='white',
                width=18,
                relief=tk.RAISED,
                bd=2,
                cursor="hand2",
                activebackground=self.BUTTON_HOVER_COLOR,
                command=lambda key=option_name: callback_function(key)
            )
            btn.pack(pady=8)

    def create_size_menu(self):
        """Crea el menú para elegir el tamaño."""
        self.create_generic_menu(
            "Paso 1: Elige el Tamaño del Destello",
            self.size_map,
            self.select_size
        )

    def create_color_menu(self):
        """Crea el menú para elegir el color."""
        self.create_generic_menu(
            "Paso 2: Elige un Color para el Destello",
            self.color_map,
            self.select_color
        )

    def create_movement_menu(self):
        """Crea el menú para elegir el tipo de movimiento."""
        self.create_generic_menu(
            "Paso 3: Elige el Tipo de Movimiento",
            self.movement_map,
            self.select_movement
        )

    # --- FUNCIONES DE SELECCIÓN (CALLBACKS) ---
    def select_size(self, chosen_size_name):
        """Guarda el tamaño elegido y pasa al siguiente menú."""
        self.flash_size = self.size_map[chosen_size_name]
        self.create_color_menu()

    def select_color(self, chosen_color_name):
        """Guarda el color elegido y pasa al siguiente menú."""
        self.flash_color = self.color_map[chosen_color_name]
        self.create_movement_menu()

    def select_movement(self, chosen_movement_name):
        """Guarda el movimiento y comienza la animación."""
        self.movement_mode = self.movement_map[chosen_movement_name]
        self.start_animation()

    def start_animation(self):
        """Inicia la animación con la configuración seleccionada."""
        self.limpiar_menu_actual()

        self.animation_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.animation_frame.pack(fill=tk.BOTH, expand=True)
        self.current_menu_frame = self.animation_frame # Actualizamos la referencia

        self.timer_label = tk.Label(
            self.animation_frame,
            text=f"Tiempo: {self.time_left}",
            font=self.default_font,
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR
        )
        self.timer_label.pack(pady=10)

        self.canvas = tk.Canvas(
            self.animation_frame, 
            bg=self.FRAME_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.is_animating = True
        self.time_left = self.animation_duration
        self.update_timer()
        self.root.after(100, self.setup_and_start_flash)

    def update_timer(self):
        if self.time_left > 0 and self.is_animating:
            self.time_left -= 1
            self.timer_label.config(text=f"Tiempo: {self.time_left}")
            self.timer_job = self.root.after(1000, self.update_timer)
        else:
            self.end_animation()

    def setup_and_start_flash(self):
        if not self.is_animating:
            return
            
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Posición inicial aleatoria
        x = random.randint(self.flash_size, canvas_width - self.flash_size)
        y = random.randint(self.flash_size, canvas_height - self.flash_size)

        self.flash_item = self.canvas.create_oval(
            x - self.flash_size, y - self.flash_size,
            x + self.flash_size, y + self.flash_size,
            fill=self.flash_color,
            outline=self.ACCENT_COLOR,
            width=2
        )

        # La velocidad inicial depende del modo de movimiento
        if self.movement_mode == 'horizontal':
            self.vx = random.choice([-self.flash_speed, self.flash_speed])
            self.vy = 0
        elif self.movement_mode == 'vertical':
            self.vx = 0
            self.vy = random.choice([-self.flash_speed, self.flash_speed])
        elif self.movement_mode == 'random':  # Movimiento aleatorio
            # Generar una dirección aleatoria
            angle = random.uniform(0, 2 * math.pi)
            self.vx = self.flash_speed * math.cos(angle)
            self.vy = self.flash_speed * math.sin(angle)

        self.move_flash()

    def move_flash(self):
        if not self.is_animating:
            return
            
        # Mover el objeto
        self.canvas.move(self.flash_item, self.vx, self.vy)
        
        # Obtener las coordenadas actuales del objeto (bounding box)
        coords = self.canvas.coords(self.flash_item)
        if not coords: return
        
        # Coordenadas de los bordes del objeto
        left_x = coords[0]
        top_y = coords[1]
        right_x = coords[2]
        bottom_y = coords[3]

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        collision_occurred = False

        # --- LÓGICA DE DETECCIÓN DE COLISIÓN Y REBOTE ---
        if self.movement_mode == 'horizontal':
            # Rebote en los bordes izquierdo y derecho
            if left_x <= 0 or right_x >= canvas_width:
                self.vx = -self.vx  # Invierte la velocidad horizontal
                collision_occurred = True
                # Corrección para evitar que se quede atascado en el borde
                if left_x <= 0:
                    self.canvas.move(self.flash_item, -left_x, 0)
                elif right_x >= canvas_width:
                    self.canvas.move(self.flash_item, canvas_width - right_x, 0)

        elif self.movement_mode == 'vertical':
            # Rebote en los bordes superior e inferior
            if top_y <= 0 or bottom_y >= canvas_height:
                self.vy = -self.vy  # Invierte la velocidad vertical
                collision_occurred = True
                # Corrección para evitar que se quede atascado en el borde
                if top_y <= 0:
                    self.canvas.move(self.flash_item, 0, -top_y)
                elif bottom_y >= canvas_height:
                    self.canvas.move(self.flash_item, 0, canvas_height - bottom_y)
        
        elif self.movement_mode == 'random':  # Movimiento aleatorio
            # Rebote en todos los bordes
            if left_x <= 0 or right_x >= canvas_width:
                self.vx = -self.vx  # Invierte la velocidad horizontal
                collision_occurred = True
                # Corrección para evitar que se quede atascado en el borde
                if left_x <= 0:
                    self.canvas.move(self.flash_item, -left_x, 0)
                elif right_x >= canvas_width:
                    self.canvas.move(self.flash_item, canvas_width - right_x, 0)
            
            if top_y <= 0 or bottom_y >= canvas_height:
                self.vy = -self.vy  # Invierte la velocidad vertical
                collision_occurred = True
                # Corrección para evitar que se quede atascado en el borde
                if top_y <= 0:
                    self.canvas.move(self.flash_item, 0, -top_y)
                elif bottom_y >= canvas_height:
                    self.canvas.move(self.flash_item, 0, canvas_height - bottom_y)
        
        # --- LÓGICA DE AUMENTO DE VELOCIDAD ---
        if collision_occurred:
            current_speed = math.sqrt(self.vx**2 + self.vy**2)
            if current_speed > 0:
                new_speed = current_speed + self.speed_increase_amount
                scale_factor = new_speed / current_speed
                self.vx *= scale_factor
                self.vy *= scale_factor

        # Programar el siguiente movimiento
        self.root.after(self.animation_delay_ms, self.move_flash)

    def end_animation(self):
        self.is_animating = False
        
        if self.timer_job:
            self.root.after_cancel(self.timer_job)

        self.timer_label.pack_forget()
        
        if hasattr(self, 'flash_item'):
            self.canvas.delete(self.flash_item)
            
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text="Seguimiento Visual Terminado",
            fill=self.ACCENT_COLOR,
            font=self.title_font
        )
        
        self.return_timer = 4
        self.return_timer_label = tk.Label(
            self.animation_frame,
            text=f"Volviendo al menú en: {self.return_timer}",
            font=self.default_font,
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR
        )
        self.return_timer_label.pack(pady=10)
        
        self.update_return_timer()

    def update_return_timer(self):
        if self.return_timer > 0:
            self.return_timer -= 1
            self.return_timer_label.config(text=f"Volviendo al menú en: {self.return_timer}")
            self.return_timer_job = self.root.after(1000, self.update_return_timer)
        else:
            if self.return_timer_job:
                self.root.after_cancel(self.return_timer_job)
            
            self.animation_frame.destroy()
            self.create_size_menu() # Vuelve al primer menú de la cadena

# --- Ejecución del Programa ---
if __name__ == "__main__":
    main_root = tk.Tk()
    app = VisualTrackingApp(main_root)
    main_root.mainloop()