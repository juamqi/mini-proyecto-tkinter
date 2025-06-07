import tkinter as tk
import time

ventana = tk.Tk()
ventana.title("App de Estudio con Pomodoro")
ventana.geometry("600x500")


# menú con opciones:


# reloj en tiempo real:
reloj = tk.Label(ventana, text="", font=("Arial", 24))
reloj.pack(pady=20, anchor='center')

def hora():
    hora_actual = time.strftime("%H:%M:%S")
    reloj.config(text=hora_actual)
    ventana.after(1000, hora)
hora()


# input para escribir y botón para agregar temas:

# lista de temas con scrollbar:

# botón de eliminar tema:


# área de pomodoro:


ventana.mainloop()