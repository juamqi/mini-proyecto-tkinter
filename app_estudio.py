import tkinter as tk
from tkinter import messagebox
import time
import math

color_fondo = "#2E2E2E"
ventana = tk.Tk()
ventana.title("App de Estudio con Pomodoro")
ventana.geometry("600x700")
ventana.config(bg=color_fondo)

reloj = tk.Label(ventana, text="", font=("Arial", 16), bg=color_fondo, fg="white")
reloj.pack(pady=10)

def hora():
    reloj.config(text="Hora actual: " + time.strftime("%H:%M:%S"))
    ventana.after(1000, hora)
    
hora()

tk.Label(ventana, text="Ingresá un tema para estudiar:", bg=color_fondo, fg="white", font=("Arial", 12)).pack(pady=(10, 0))
entrada_tema = tk.Entry(ventana, width=40, font=("Arial", 12))
entrada_tema.pack(pady=5)

frame_lista = tk.Frame(ventana)
frame_lista.pack(pady=5)

scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_temas = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, width=50, height=6, font=("Arial", 12))
lista_temas.pack(side=tk.LEFT)
scrollbar.config(command=lista_temas.yview)

def agregar_tema():
    tema = entrada_tema.get().strip()
    if tema:
        lista_temas.insert(tk.END, tema)
        entrada_tema.delete(0, tk.END)

def eliminar_tema():
    seleccion = lista_temas.curselection()
    if seleccion:
        lista_temas.delete(seleccion)

frame_botones_temas = tk.Frame(ventana, bg=color_fondo)
frame_botones_temas.pack(pady=5)

tk.Button(frame_botones_temas, text="Agregar tema", command=agregar_tema, font=("Arial", 10)).pack(side="left", padx=5)
tk.Button(frame_botones_temas, text="Eliminar tema", command=eliminar_tema, font=("Arial", 10)).pack(side="left", padx=5)

tiempo_trabajo = 25 * 60
descanso_corto = 5 * 60
descanso_largo = 15 * 60

FUENTE = ("Arial", 30)
BOTON_COLOR_BG = "#4CAF50"
BOTON_COLOR_FG = "white"
BOTON_FONT = ("Arial", 12, "bold")
BOTON_ANCHO = 18
BOTON_ALTO = 2
BOTON_ACTIVO = "#45a049"

repeticiones = 0
temporizador = None
en_pausa = False
tiempo_restante = 0
tema_actual = ""

def crear_boton(texto, comando):
    return tk.Button(
        text=texto,
        command=comando,
        bg=BOTON_COLOR_BG,
        fg=BOTON_COLOR_FG,
        font=BOTON_FONT,
        width=BOTON_ANCHO,
        height=BOTON_ALTO,
        activebackground=BOTON_ACTIVO,
        relief="raised",
        bd=3,
        highlightthickness=0
    )

def iniciar_temporizador():
    global repeticiones, en_pausa, tiempo_restante, temporizador, tema_actual

    seleccion = lista_temas.curselection()
    if not seleccion:
        messagebox.showwarning("Seleccioná un tema", "Debés seleccionar un tema antes de iniciar el Pomodoro.")
        return

    tema_actual = lista_temas.get(seleccion)
    etiqueta_tema_estudio.config(text=f"Estudiando: {tema_actual}")

    if temporizador:
        ventana.after_cancel(temporizador)
        temporizador = None

    if not en_pausa:
        repeticiones += 1
        if repeticiones % 8 == 0:
            tiempo_restante = descanso_largo
            etiqueta_titulo.config(text="Descanso largo", fg="red")
        elif repeticiones % 2 == 0:
            tiempo_restante = descanso_corto
            etiqueta_titulo.config(text="Descanso corto", fg="green")
        else:
            tiempo_restante = tiempo_trabajo
            etiqueta_titulo.config(text="Trabajo", fg="brown")

    en_pausa = False
    cuenta_regresiva(tiempo_restante)

def cuenta_regresiva(tiempo):
    global temporizador, tiempo_restante
    minutos = math.floor(tiempo / 60)
    segundos = tiempo % 60
    if segundos < 10:
        segundos = f"0{segundos}"
    etiqueta_tiempo.config(text=f"{minutos}:{segundos}")
    if tiempo > 0:
        tiempo_restante = tiempo - 1
        temporizador = ventana.after(1000, cuenta_regresiva, tiempo_restante)
    else:
        actualizar_marcas()
        iniciar_temporizador()

def reiniciar_temporizador():
    global repeticiones, en_pausa, tiempo_restante, tema_actual
    ventana.after_cancel(temporizador)
    etiqueta_titulo.config(text="Temporizador", fg="white")
    etiqueta_tiempo.config(text="25:00")
    etiqueta_marcas.config(text="")
    etiqueta_tema_estudio.config(text="Estudiando: -")
    repeticiones = 0
    en_pausa = False
    tiempo_restante = 0
    tema_actual = ""

def pausar_temporizador():
    global en_pausa
    if not en_pausa:
        ventana.after_cancel(temporizador)
        en_pausa = True
        etiqueta_titulo.config(text="Pausado", fg="blue")
    else:
        if repeticiones % 8 == 0:
            etiqueta_titulo.config(text="Descanso largo", fg="yellow")
        elif repeticiones % 2 == 0:
            etiqueta_titulo.config(text="Descanso corto", fg="white")
        else:
            etiqueta_titulo.config(text="Trabajo", fg="purple")
        en_pausa = False
        cuenta_regresiva(tiempo_restante)

def actualizar_marcas():
    sesiones_trabajo = math.floor(repeticiones / 2)
    marcas = "✔" * sesiones_trabajo
    etiqueta_marcas.config(text=marcas)

contenedor_pomodoro = tk.Frame(ventana, bg=color_fondo)
contenedor_pomodoro.pack(pady=20)
frame_botones = tk.Frame(contenedor_pomodoro, bg=color_fondo)
frame_botones.pack(pady=10)

frame_botones_extra = tk.Frame(contenedor_pomodoro, bg=color_fondo)
frame_botones_extra.pack(pady=10)
etiqueta_titulo = tk.Label(contenedor_pomodoro, text="Temporizador", font=("Arial", 36), bg=color_fondo, fg="white")
etiqueta_titulo.pack(pady=10)

etiqueta_tiempo = tk.Label(contenedor_pomodoro, text="25:00", font=("Arial", 48), bg=color_fondo, fg="white")
etiqueta_tiempo.pack(pady=10)

etiqueta_tema_estudio = tk.Label(contenedor_pomodoro, text="Estudiando: -", font=("Arial", 16), bg=color_fondo, fg="lightblue")
etiqueta_tema_estudio.pack(pady=5)

etiqueta_marcas = tk.Label(contenedor_pomodoro, font=("Arial", 20), bg=color_fondo, fg="lightgrey")
etiqueta_marcas.pack(pady=10)

crear_boton("Iniciar Pomodoro", iniciar_temporizador).pack(in_=frame_botones, side="left", padx=5)
crear_boton("Pausar / Reanudar", pausar_temporizador).pack(in_=frame_botones, side="left", padx=5)
crear_boton("Reiniciar", reiniciar_temporizador).pack(in_=frame_botones, side="left", padx=5)

ventana.mainloop()