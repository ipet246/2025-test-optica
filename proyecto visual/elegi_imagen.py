import tkinter as tk
from PIL import Image, ImageTk
import random

# --- Lista de imágenes posibles (usa tus archivos PNG reales con fondo transparente) ---
imagenes = ["casaa.jpg", "paraguass.webp", "manzanaa.jpg", "avionn.jpg"]

# --- Variables globales ---
imagen_actual_tk = None
nombre_imagen_actual = ""
tiempo_restante = 10
temporizador_id = None
puntos = 0
juego_activo = True

# --- Mapeo imagen -> tecla correcta (minúscula) ---
mapeo_teclas = {
    "manzanaa.jpg": "m",
    "paraguass.webp": "p",
    "casaa.jpg": "c",
    "avionn.jpg": "a"
}


def mover_boton():
    global imagen_actual_tk, nombre_imagen_actual, tiempo_restante, temporizador_id, juego_activo

    if not juego_activo:
        return

    tiempo_restante = 10
    actualizar_tiempo()

    if temporizador_id:
        ventana.after_cancel(temporizador_id)

    ventana.update_idletasks()

    # --- Elegir imagen aleatoria ---
    nombre_imagen_actual = random.choice(imagenes)
    try:
        img = Image.open(nombre_imagen_actual)
    except Exception as e:
        resultado.config(text=f"Error al abrir {nombre_imagen_actual}: {e}", fg="red")
        return

    # --- Redimensionar manteniendo proporción ---
    max_w, max_h = 240, 140
    img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)

    imagen_actual_tk = ImageTk.PhotoImage(img)

    # --- Configurar botón con imagen como fondo ---
    boton.config(
        image=imagen_actual_tk,
        text="",
        compound="center",
        bg="white",
        activebackground="black",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        width=imagen_actual_tk.width(),
        height=imagen_actual_tk.height()
    )

    # --- Calcular posición aleatoria dentro de un área segura ---
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    btn_w = imagen_actual_tk.width()
    btn_h = imagen_actual_tk.height()

    # Margen superior (zona donde están las etiquetas)
    zona_segura_superior = 250  # píxeles desde arriba (ajústalo si lo necesitas)
    zona_segura_inferior = 100  # margen inferior para no ir muy abajo

    # Calcular coordenadas aleatorias dentro del área visible y segura
    x = random.randint(50, max(50, ancho_pantalla - btn_w - 50))
    y = random.randint(zona_segura_superior, max(zona_segura_superior, alto_pantalla - btn_h - zona_segura_inferior))

    boton.place(x=x, y=y)


    temporizador_id = ventana.after(1000, contar_tiempo)


def contar_tiempo():
    global tiempo_restante, temporizador_id
    if not juego_activo:
        return

    tiempo_restante -= 1
    actualizar_tiempo()

    if tiempo_restante <= 0:
        perder_juego()
    else:
        temporizador_id = ventana.after(1000, contar_tiempo)


def actualizar_tiempo():
    tiempo_label.config(text=f"Tiempo: {tiempo_restante}s")


def actualizar_puntaje():
    puntaje_label.config(text=f"Puntaje: {puntos}")


def tecla_presionada(event):
    global temporizador_id, puntos, nombre_imagen_actual
    if not juego_activo:
        return

    tecla = (event.char or event.keysym).lower()
    correcta = mapeo_teclas.get(nombre_imagen_actual, None)

    if correcta and tecla == correcta:
        resultado.config(text=f"✅ ¡Correcto! ({nombre_imagen_actual})", fg="lime",bg="white")
        puntos += 1
        actualizar_puntaje()
        if temporizador_id:
            ventana.after_cancel(temporizador_id)
        mover_boton()
    else:
        espera = correcta if correcta else "?"
        resultado.config(text=f"❌ Incorrecto ({tecla.upper()}) — esperada: {espera.upper()}", fg="red",bg="white")
        puntos -= 1
        actualizar_puntaje()


def perder_juego():
    global juego_activo
    juego_activo = False

    if temporizador_id:
        ventana.after_cancel(temporizador_id)

    boton.place_forget()
    resultado.config(text="😢 ¡Se acabó el tiempo! Perdiste.", fg="orange",bg="white")
    tiempo_label.pack_forget()
    puntaje_label.pack_forget()

    mostrar_pantalla_final()


def mostrar_pantalla_final():
    frame_final = tk.Frame(ventana, bg="white")
    frame_final.pack(expand=True)

    mensaje_final = tk.Label(
        frame_final,
        text=f"¡Perdiste! 😞\nPuntaje final: {puntos}",
        bg="white", fg="black", font=("Arial", 30, "bold")
    )
    mensaje_final.pack(pady=40)

    boton_reintentar = tk.Button(
        frame_final, text="Volver a jugar", font=("Arial", 20, "bold"),
        bg="green", fg="black", width=15, height=2,
        command=lambda: reiniciar_juego(frame_final)
    )
    boton_reintentar.pack(pady=20)

    boton_salir = tk.Button(
        frame_final, text="Salir", font=("Arial", 20, "bold"),
        bg="red", fg="black", width=15, height=2,
        command=ventana.destroy
    )
    boton_salir.pack(pady=10)


def reiniciar_juego(frame_final):
    global puntos, juego_activo

    frame_final.destroy()
    puntos = 0
    juego_activo = True
    actualizar_puntaje()
    resultado.config(text="")
    tiempo_label.pack(side="left", padx=50)
    puntaje_label.pack(side="right", padx=50)

    mover_boton()


# --- Crear ventana principal ---
ventana = tk.Tk()
ventana.title("Juego de Imágenes - Reacción Rápida")
ventana.attributes("-fullscreen", True)
ventana.config(bg="white")

instrucciones = tk.Label(
    ventana,
    text="Presiona la tecla correcta según la imagen:\nManzana → M | Paraguas → P | Casa → C | Avión → A",
    bg="white", fg="black", font=("Arial", 26)
)
instrucciones.pack(pady=20)

frame_info = tk.Frame(ventana, bg="white")
frame_info.pack(pady=10)

tiempo_label = tk.Label(frame_info, text="Tiempo: 10s", bg="white", fg="black", font=("Arial", 22, "bold"))
tiempo_label.pack(side="left", padx=50)

puntaje_label = tk.Label(frame_info, text="Puntaje: 0", bg="white", fg="black", font=("Arial", 22, "bold"))
puntaje_label.pack(side="right", padx=50)

resultado = tk.Label(ventana, text="", bg="white", fg="black", font=("Arial", 22, "bold"))
resultado.pack(pady=25)

# --- Botón con imagen de fondo transparente ---
boton = tk.Button(
    ventana,
    text="",
    bg="white",
    fg="black",
    font=("Arial", 28, "bold"),
    borderwidth=0,
    highlightthickness=0,
    relief="flat",
    command=mover_boton
)
boton.place(x=500, y=300)

ventana.bind_all("<Key>", tecla_presionada)
ventana.focus_set()

ventana.after(200, mover_boton)

ventana.mainloop()
