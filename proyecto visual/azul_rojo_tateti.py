import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Cajas Superpuestas con Transparencia")
ventana.geometry("800x500")
ventana.config(bg="white")

# Crear lienzo (canvas)
canvas = tk.Canvas(ventana, width=800, height=500)
canvas.pack()

# Crear imagen base blanca
imagen = Image.new("RGBA", (800, 500), (255, 255, 255, 255))
draw = ImageDraw.Draw(imagen)

# Dibujar cajas con transparencia (R,G,B,Alpha)
draw.rectangle((100, 100, 500, 400), fill=(255, 0, 0, 150))   # Roja semitransparente
draw.rectangle((300, 200, 700, 450), fill=(0, 0, 255, 150))   # Azul semitransparente
draw.rectangle((200, 150, 600, 430), fill=(0, 0, 0, 80))      # Negra muy transparente

# Convertir a formato para Tkinter
imagen_tk = ImageTk.PhotoImage(imagen)
canvas.create_image(0, 0, anchor="nw", image=imagen_tk)

# Texto sobre cada zona
canvas.create_text(300, 250, text="Mensaje en la caja ROJA", fill="white",
                   font=("Arial", 24, "bold"))
canvas.create_text(500, 300, text="Mensaje en la caja AZUL", fill="yellow",
                   font=("Arial", 24, "bold"))

ventana.mainloop()
