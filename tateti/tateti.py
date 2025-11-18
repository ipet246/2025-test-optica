import tkinter as tk
from tkinter import font
import random

class TatetiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tateti Moderno")
        
        # --- Configuración de la ventana ---
        # Se permite redimensionar y se establece un tamaño mínimo para que no se rompa.
        self.root.minsize(400, 500)
        self.root.resizable(True, True)

        # --- Paleta de Colores Moderna ---
        self.BG_COLOR = '#1a1a2e'
        self.FRAME_COLOR = '#16213e'
        # --- CAMBIO: Color de los botones a gris ---
        self.BUTTON_COLOR = '#5a5a5a'  # Gris para los botones/cuadrados
        self.BUTTON_HOVER_COLOR = '#7a7a7a' # Gris más claro para el hover
        # --- CAMBIO: Color de la X a verde ---
        self.X_COLOR = '#2ecc71'  # Verde para la X
        self.O_COLOR = '#E74C3C'  # Rojo para el Círculo
        self.TEXT_COLOR = '#ECF0F1'
        self.ACCENT_COLOR = '#16c79a'
        self.STATUS_BG_COLOR = '#0f3460'
        self.TIMER_BG_COLOR = '#2c3e50'

        self.root.configure(bg=self.BG_COLOR)

        # --- Variables del Juego ---
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        # --- CAMBIO: Tiempo inicial aumentado a 20 segundos ---
        self.time_left = 20
        self.timer_job = None
        self.game_mode = None  # 'pvp' or 'bot'
        self.bot_player = 'O'
        self.human_player = 'X'

        # --- Fuentes ---
        self.game_font = font.Font(family="Helvetica", size=36, weight="bold")
        self.status_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.welcome_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.winner_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.timer_font = font.Font(family="Courier", size=20, weight="bold")
        self.menu_font = font.Font(family="Helvetica", size=16, weight="bold")

        # --- Crear la interfaz inicial ---
        self.create_start_menu()
        
        # --- Mapeo del teclado numérico ---
        self.key_map = {
            '7': (0, 0), '8': (0, 1), '9': (0, 2),
            '4': (1, 0), '5': (1, 1), '6': (1, 2),
            '1': (2, 0), '2': (2, 1), '3': (2, 2)
        }
        self.root.bind('<KeyPress>', self.handle_keypress)

    def create_start_menu(self):
        self.start_menu_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.start_menu_frame.pack(fill=tk.BOTH, expand=True)

        # --- CAMBIO: Texto de inicio modificado ---
        title_label = tk.Label(
            self.start_menu_frame,
            text="¡Juega al Ta-Te-Ti!",
            font=self.welcome_font,
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR
        )
        title_label.pack(pady=20)

        rules_frame = tk.Frame(self.start_menu_frame, bg=self.BG_COLOR)
        rules_frame.pack(pady=10)

        # --- CAMBIO: Texto de reglas actualizado ---
        rules_text = (
            "Cada jugador tiene 20 segundos\n"
            "para realizar su movimiento.\n"
            "¡Si no lo haces, perderás tu turno!"
        )
        rules_label = tk.Label(
            rules_frame,
            text=rules_text,
            font=self.menu_font,
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR,
            justify=tk.CENTER
        )
        rules_label.pack()

        # --- NUEVO: Gráfica de controles ---
        legend_frame = tk.Frame(self.start_menu_frame, bg=self.BG_COLOR)
        legend_frame.pack(pady=10)
        
        legend_title = tk.Label(
            legend_frame,
            text="Controles (Teclado Numérico):",
            font=self.menu_font,
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR
        )
        legend_title.pack()

        legend_grid = tk.Frame(legend_frame, bg=self.BG_COLOR)
        legend_grid.pack(pady=5)

        legend_map = {
            '7': (0, 0), '8': (0, 1), '9': (0, 2),
            '4': (1, 0), '5': (1, 1), '6': (1, 2),
            '1': (2, 0), '2': (2, 1), '3': (2, 2)
        }
        for key, (r, c) in legend_map.items():
            label = tk.Label(
                legend_grid,
                text=key,
                font=self.menu_font,
                bg=self.BUTTON_COLOR,
                fg=self.TEXT_COLOR,
                width=4,
                height=2,
                relief=tk.RAISED,
                bd=1
            )
            label.grid(row=r, column=c, padx=2, pady=2)

        button_frame = tk.Frame(self.start_menu_frame, bg=self.BG_COLOR)
        button_frame.pack(pady=20)

        pvp_button = tk.Button(
            button_frame,
            text="1 vs 1 (Dos Jugadores)",
            font=self.menu_font,
            command=self.start_pvp_game,
            bg=self.ACCENT_COLOR,
            fg=self.BG_COLOR,
            relief=tk.FLAT,
            bd=0,
            activebackground='#13a383',
            padx=20,
            pady=10
        )
        pvp_button.pack(pady=10)

        bot_button = tk.Button(
            button_frame,
            text="1 vs Bot (Contra la IA)",
            font=self.menu_font,
            command=self.start_bot_game,
            bg=self.BUTTON_COLOR,
            fg=self.TEXT_COLOR,
            relief=tk.FLAT,
            bd=0,
            activebackground=self.BUTTON_HOVER_COLOR,
            padx=20,
            pady=10
        )
        bot_button.pack(pady=10)

    def create_game_board(self):
        self.game_frame = tk.Frame(self.root, bg=self.FRAME_COLOR, relief=tk.RAISED, bd=2)
        
        top_frame = tk.Frame(self.game_frame, bg=self.FRAME_COLOR)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.timer_frame = tk.Frame(top_frame, bg=self.TIMER_BG_COLOR, relief=tk.SOLID, bd=1)
        self.timer_frame.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        
        # --- CAMBIO: Texto inicial del temporizador a 20s ---
        self.timer_label = tk.Label(
            self.timer_frame,
            text="20s",
            font=self.timer_font,
            fg=self.TEXT_COLOR,
            bg=self.TIMER_BG_COLOR,
            padx=10,
            pady=5
        )
        self.timer_label.pack()

        self.status_label = tk.Label(
            top_frame,
            text="",
            font=self.status_font,
            bg=self.STATUS_BG_COLOR,
            fg=self.TEXT_COLOR,
            pady=10
        )
        self.status_label.pack(fill=tk.X, expand=True)
        self.update_status()

        board_frame = tk.Frame(self.game_frame, bg=self.FRAME_COLOR)
        board_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        for i in range(3):
            board_frame.grid_rowconfigure(i, weight=1)
            board_frame.grid_columnconfigure(i, weight=1)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    board_frame,
                    text='',
                    font=self.game_font,
                    bg=self.BUTTON_COLOR,
                    fg=self.TEXT_COLOR,
                    relief=tk.FLAT,
                    bd=0,
                    activebackground=self.BUTTON_HOVER_COLOR,
                    command=lambda r=i, c=j: self.player_move(r, c)
                )
                btn.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                self.buttons[i][j] = btn

        self.game_over_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        
        self.winner_label = tk.Label(
            self.game_over_frame,
            text="",
            font=self.winner_font,
            bg=self.BG_COLOR,
            fg=self.ACCENT_COLOR
        )
        self.winner_label.pack(pady=50)

        menu_button = tk.Button(
            self.game_over_frame,
            text="Volver al Menú",
            font=self.status_font,
            command=self.show_start_menu,
            bg=self.ACCENT_COLOR,
            fg=self.BG_COLOR,
            relief=tk.FLAT,
            bd=0,
            activebackground='#13a383',
            padx=20,
            pady=10
        )
        menu_button.pack()

    def start_pvp_game(self):
        self.game_mode = 'pvp'
        self.start_new_game()

    def start_bot_game(self):
        self.game_mode = 'bot'
        self.start_new_game()

    def start_new_game(self):
        if hasattr(self, 'start_menu_frame'):
            self.start_menu_frame.pack_forget()
        if hasattr(self, 'game_over_frame'):
            self.game_over_frame.pack_forget()
        
        if not hasattr(self, 'game_frame'):
            self.create_game_board()
            
        self.game_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.reset_board()
        self.update_status()
        self.start_timer()

    def show_start_menu(self):
        if hasattr(self, 'game_frame'):
            self.game_frame.pack_forget()
        if hasattr(self, 'game_over_frame'):
            self.game_over_frame.pack_forget()
        
        self.start_menu_frame.pack(fill=tk.BOTH, expand=True)
        if self.timer_job:
            self.root.after_cancel(self.timer_job)

    def reset_board(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        # --- CAMBIO: Tiempo de reinicio a 20 segundos ---
        self.time_left = 20
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = ''
                self.buttons[i][j]['fg'] = self.TEXT_COLOR
                self.buttons[i][j]['state'] = 'normal'
        
        self.timer_label.config(fg=self.TEXT_COLOR)

    def handle_keypress(self, event):
        if self.game_over or (self.game_mode == 'bot' and self.current_player == self.bot_player):
            return

        key = event.char
        if key in self.key_map:
            row, col = self.key_map[key]
            self.player_move(row, col)

    def update_status(self):
        if self.game_over:
            return
        
        if self.game_mode == 'pvp':
            # --- CAMBIO: Texto de estado actualizado a los nuevos colores ---
            player_name = "Jugador X (Verde)" if self.current_player == 'X' else "Jugador O (Rojo)"
        else: # bot mode
            if self.current_player == self.human_player:
                player_name = "Tu Turno (Jugador X)"
            else:
                player_name = "Turno del Bot (Jugador O)"
        
        self.status_label.config(text=f"Turno de {player_name}")

    def update_timer_display(self):
        if self.game_over or (self.game_mode == 'bot' and self.current_player == self.bot_player):
            self.timer_frame.pack_forget()
            return
            
        self.timer_frame.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        self.timer_label.config(text=f"{self.time_left}s")
        
        if self.time_left <= 5:
            self.timer_label.config(fg=self.O_COLOR)
        else:
            self.timer_label.config(fg=self.TEXT_COLOR)

    def player_move(self, row, col):
        if self.game_over or self.board[row][col] != '':
            return

        self.place_mark(row, col)
        if not self.check_game_over():
            self.switch_turn()

    def place_mark(self, row, col):
        self.board[row][col] = self.current_player
        
        if self.current_player == 'X':
            mark_text = 'X'
            color = self.X_COLOR
        else:
            mark_text = 'O'
            color = self.O_COLOR
            
        self.buttons[row][col]['text'] = mark_text
        self.buttons[row][col]['fg'] = color
        self.buttons[row][col]['disabledforeground'] = color
        self.buttons[row][col]['state'] = 'disabled'

    def switch_turn(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.update_status()
        
        if self.game_mode == 'bot' and self.current_player == self.bot_player:
            if self.timer_job:
                self.root.after_cancel(self.timer_job)
            self.timer_frame.pack_forget()
            self.root.after(500, self.bot_move)
        else:
            # --- CAMBIO: Tiempo de reinicio al cambiar de turno a 20 segundos ---
            self.time_left = 20
            self.start_timer()

    def start_timer(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        self.update_timer()

    def update_timer(self):
        if self.game_over or (self.game_mode == 'bot' and self.current_player == self.bot_player):
            return

        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer_display()
            self.timer_job = self.root.after(1000, self.update_timer)
        else:
            # --- NUEVO COMPORTAMIENTO: El tiempo se acabó, se pierde el turno ---
            empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == '']
            if empty_cells:
                row, col = random.choice(empty_cells)
                self.place_mark(row, col) # Coloca la marca del jugador que perdió el turno
            
            if not self.check_game_over():
                self.switch_turn()

    def bot_move(self):
        move = self.find_best_move()
        if move:
            row, col = move
            self.place_mark(row, col)
            if not self.check_game_over():
                self.switch_turn()

    def find_best_move(self):
        # 1. Intentar ganar
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == '':
                    self.board[r][c] = self.bot_player
                    if self.check_winner_for_player(self.bot_player):
                        self.board[r][c] = ''
                        return (r, c)
                    self.board[r][c] = ''

        # 2. Intentar bloquear al jugador
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == '':
                    self.board[r][c] = self.human_player
                    if self.check_winner_for_player(self.human_player):
                        self.board[r][c] = ''
                        return (r, c)
                    self.board[r][c] = ''

        # 3. Tomar el centro
        if self.board[1][1] == '':
            return (1, 1)

        # 4. Tomar una esquina
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [c for c in corners if self.board[c[0]][c[1]] == '']
        if available_corners:
            return random.choice(available_corners)

        # 5. Tomar un lado
        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
        available_sides = [s for s in sides if self.board[s[0]][s[1]] == '']
        if available_sides:
            return random.choice(available_sides)
        
        return None

    def check_winner_for_player(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def check_game_over(self):
        winner = None
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                winner = self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                winner = self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            winner = self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            winner = self.board[0][2]

        if winner:
            if self.game_mode == 'bot':
                winner_name = "¡Tú ganas!" if winner == self.human_player else "¡El Bot gana!"
            else:
                winner_name = f"¡El jugador {winner} ha ganado!"
            self.end_game(winner_name)
            return True

        if all(self.board[r][c] != '' for r in range(3) for c in range(3)):
            self.end_game("¡Es un empate!")
            return True
            
        return False

    def end_game(self, message):
        self.game_over = True
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        
        self.winner_label.config(text=message)
        
        self.game_frame.pack_forget()
        self.game_over_frame.pack(fill=tk.BOTH, expand=True)

# --- Ejecución del Programa ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TatetiApp(root)
    root.mainloop()