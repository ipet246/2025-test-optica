import tkinter as tk
import random

# Colores posibles
colores = ["red", "green", "yellow","blue","orange","purple"]

# Variables globales
color_actual = ""
tiempo_restante = 10
temporizador_id = None
puntos = 0
juego_activo = True


# Función para mover el botón y cambiar color
def mover_boton():
    global color_actual, tiempo_restante, temporizador_id, juego_activo

    if not juego_activo:
        return  # Si el juego terminó, no hacer nada

    # Reiniciar tiempo
    tiempo_restante = 10
    actualizar_tiempo()

    # Cancelar temporizador anterior si existe
    if temporizador_id:
        ventana.after_cancel(temporizador_id)

    # Actualizar geometría
    ventana.update_idletasks()

    # Elegir nuevo color
    color_actual = random.choice(colores)
    boton.config(bg=color_actual)

    # --- Calcular posición aleatoria dentro de un área segura ---
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    btn_w = boton.winfo_reqwidth()
    btn_h = boton.winfo_reqheight()

    # Margen superior donde están las etiquetas
    zona_segura_superior = 250   # píxeles desde arriba
    zona_segura_inferior = 100   # margen inferior (por si acaso)
    margen_lateral = 50          # no pegarse a los bordes

    # Calcular coordenadas aleatorias dentro del área visible y segura
    x = random.randint(margen_lateral, max(margen_lateral, ancho_pantalla - btn_w - margen_lateral))
    y = random.randint(zona_segura_superior, max(zona_segura_superior, alto_pantalla - btn_h - zona_segura_inferior))

    boton.place(x=x, y=y)


    # Iniciar temporizador
    temporizador_id = ventana.after(1000, contar_tiempo)


# Contador de tiempo
def contar_tiempo():
    global tiempo_restante, temporizador_id, puntos

    if not juego_activo:
        return

    tiempo_restante -= 1
    actualizar_tiempo()

    if tiempo_restante <= 0:
        perder_juego()
    else:
        temporizador_id = ventana.after(1000, contar_tiempo)


# Actualizar texto del contador
def actualizar_tiempo():
    tiempo_label.config(text=f"Tiempo: {tiempo_restante}s")


# Actualizar puntaje
def actualizar_puntaje():
    puntaje_label.config(text=f"Puntaje: {puntos}")


# Verificar la tecla presionada
def tecla_presionada(event):
    global temporizador_id, puntos
    if not juego_activo:
        return
    tecla2 = event.char.lower()

    tecla = event.keysym.lower()

    correcto = (
        (color_actual == "yellow" and tecla == "1") or
        (color_actual == "red" and tecla == "5") or
        (color_actual == "green" and tecla == "9") or
        (color_actual == "blue" and tecla == "z") or
        (color_actual == "orange" and tecla == "b") or
        (color_actual == "purple" and tecla2 == ".")
    )

    if correcto:
        resultado.config(text=f"✅ ¡Correcto! ({color_actual.upper()})", fg="lime")
        puntos += 1
        actualizar_puntaje()
        if temporizador_id:
            ventana.after_cancel(temporizador_id)
        mover_boton()
    else:
        resultado.config(text=f"❌ Incorrecto ({tecla.upper()})", fg="red")
        puntos -= 1
        actualizar_puntaje()


# Función cuando el tiempo se acaba (pierde)
def perder_juego():
    global juego_activo
    juego_activo = False

    if temporizador_id:
        ventana.after_cancel(temporizador_id)

    # Ocultar elementos del juego
    boton.place_forget()
    resultado.config(text="😢 ¡Se acabó el tiempo! Perdiste.", fg="orange")
    tiempo_label.pack_forget()
    puntaje_label.pack_forget()

    # Mostrar pantalla final
    mostrar_pantalla_final()


# Mostrar pantalla de final
def mostrar_pantalla_final():
    frame_final = tk.Frame(ventana, bg="black")
    frame_final.pack(expand=True)

    mensaje_final = tk.Label(
        frame_final,
        text=f"¡Perdiste! 😞\nPuntaje final: {puntos}",
        bg="black", fg="white", font=("Arial", 30, "bold")
    )
    mensaje_final.pack(pady=40)

    boton_reintentar = tk.Button(
        frame_final, text="Volver a jugar", font=("Arial", 20, "bold"),
        bg="green", fg="white", width=15, height=2,
        command=lambda: reiniciar_juego(frame_final)
    )
    boton_reintentar.pack(pady=20)

    boton_salir = tk.Button(
        frame_final, text="Salir", font=("Arial", 20, "bold"),
        bg="red", fg="white", width=15, height=2,
        command=ventana.destroy
    )
    boton_salir.pack(pady=10)


# Reiniciar el juego
def reiniciar_juego(frame_final):
    global puntos, juego_activo

    # Eliminar la pantalla final
    frame_final.destroy()

    # Reiniciar valores
    puntos = 0
    juego_activo = True
    actualizar_puntaje()
    resultado.config(text="")
    tiempo_label.pack(side="left", padx=50)
    puntaje_label.pack(side="right", padx=50)

    # Volver a iniciar
    mover_boton()


# Crear ventana principal
ventana = tk.Tk()
ventana.title("Juego de Colores - Reacción Rápida")

# Pantalla completa
ventana.attributes("-fullscreen", True)
ventana.config(bg="black")

# Instrucciones
instrucciones = tk.Label(
    ventana,
    text="Presiona la tecla correcta según el color:\nRojo →y | Verde → p | Amarillo → w",
    bg="black", fg="white", font=("Arial", 26)
)
instrucciones.pack(pady=20)

# Contadores (arriba de todo)
frame_info = tk.Frame(ventana, bg="black")
frame_info.pack(pady=10)

tiempo_label = tk.Label(frame_info, text="Tiempo: 10s", bg="black", fg="white", font=("Arial", 22, "bold"))
tiempo_label.pack(side="left", padx=50)

puntaje_label = tk.Label(frame_info, text="Puntaje: 0", bg="black", fg="white", font=("Arial", 22, "bold"))
puntaje_label.pack(side="right", padx=50)

# Resultado
resultado = tk.Label(ventana, text="", bg="black", fg="white", font=("Arial", 22, "bold"))
resultado.pack(pady=25)

# Botón
boton = tk.Button(
    ventana, text="¡Color!", command=mover_boton,
    bg="red", fg="white", font=("Arial", 28, "bold"), width=10, height=2
)
boton.place(x=500, y=300)

# Vincular teclas
ventana.bind_all("<Key>", tecla_presionada)
ventana.focus_set()

# Iniciar primer color
ventana.after(200, mover_boton)

ventana.mainloop()
