import tkinter as tk
import math

# ---------------------------- CONSTANTES -------------------------------
# Duraciones en segundos
tiempo_trabajo = 25 * 60
descanso_corto = 5 * 60
descanso_largo = 15 * 60

# Colores y fuente para la interfaz
color_fondo = "#2E2E2E"
FUENTE = ("Arial", 30)

# Estilo de los botones
BOTON_COLOR_BG = "#4CAF50"
BOTON_COLOR_FG = "white"
BOTON_FONT = ("Arial", 12, "bold")
BOTON_ANCHO = 18
BOTON_ALTO = 2
BOTON_ACTIVO = "#45a049"

# ---------------------------- VARIABLES GLOBALES ------------------------
repeticiones = 0           # Cuenta cuántas sesiones han pasado
temporizador = None        # Referencia al temporizador actual
en_pausa = False           # Indica si está en pausa
tiempo_restante = 0        # Cuánto tiempo queda en la cuenta regresiva

# ---------------------------- FUNCIONES -------------------------------

# Crea una función para que todos los botones tengan estilo consistente
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

# Inicia la cuenta regresiva según el tipo de sesión (trabajo o descanso)
def iniciar_temporizador():
    global repeticiones, en_pausa, tiempo_restante, temporizador

    # Si hay un temporizador en curso, cancelarlo
    if temporizador:
        ventana.after_cancel(temporizador)
        temporizador = None

    # Si no está pausado, avanzar al siguiente período
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

# Cuenta regresivamente y actualiza el texto del reloj
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

# Reinicia todo a su estado inicial
def reiniciar_temporizador():
    global repeticiones, en_pausa, tiempo_restante
    ventana.after_cancel(temporizador)
    etiqueta_titulo.config(text="Temporizador", fg="white")
    etiqueta_tiempo.config(text="25:00")
    etiqueta_marcas.config(text="")
    repeticiones = 0
    en_pausa = False
    tiempo_restante = 0

# Pausa o reanuda el temporizador
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

# Salta directamente a un descanso corto o largo
def forzar_descanso(tipo):
    global tiempo_restante, en_pausa, temporizador

    if temporizador:
        ventana.after_cancel(temporizador)
        temporizador = None

    if tipo == "corto":
        tiempo_restante = descanso_corto
        etiqueta_titulo.config(text="Descanso corto", fg="pink")
    elif tipo == "largo":
        tiempo_restante = descanso_largo
        etiqueta_titulo.config(text="Descanso largo", fg="orange")

    en_pausa = False
    cuenta_regresiva(tiempo_restante)

# Salta directamente a una sesión de trabajo
def forzar_trabajo():
    global tiempo_restante, en_pausa, temporizador

    if temporizador:
        ventana.after_cancel(temporizador)
        temporizador = None

    tiempo_restante = tiempo_trabajo
    etiqueta_titulo.config(text="Trabajo", fg="Turquoise")
    en_pausa = False
    cuenta_regresiva(tiempo_restante)

# Actualiza los "✔" por cada sesión completada
def actualizar_marcas():
    sesiones_trabajo = math.floor(repeticiones / 2)
    marcas = "✔" * sesiones_trabajo
    etiqueta_marcas.config(text=marcas)

# ---------------------------- INTERFAZ DE USUARIO -------------------------------

# Ventana principal
ventana = tk.Tk()
ventana.title("Temporizador Pomodoro")
ventana.config(padx=50, pady=25, bg=color_fondo)

# Etiquetas principales
etiqueta_titulo = tk.Label(text="Temporizador", font=("Arial", 40), bg=color_fondo, fg="white")
etiqueta_titulo.grid(column=1, row=0)

etiqueta_tiempo = tk.Label(text="25:00", font=("Arial", 48), bg=color_fondo, fg="white")
etiqueta_tiempo.grid(column=1, row=1)

etiqueta_marcas = tk.Label(font=("Arial", 20), bg=color_fondo, fg="lightgrey")
etiqueta_marcas.grid(column=1, row=3)

# Botones con estilos
crear_boton("Iniciar", iniciar_temporizador).grid(column=0, row=2)
crear_boton("Pausar/Reanudar", pausar_temporizador).grid(column=1, row=2)
crear_boton("Reiniciar", reiniciar_temporizador).grid(column=2, row=2)

crear_boton("Descanso corto", lambda: forzar_descanso("corto")).grid(column=0, row=4)
crear_boton("Descanso largo", lambda: forzar_descanso("largo")).grid(column=2, row=4)
crear_boton("Volver a trabajo", forzar_trabajo).grid(column=1, row=5)

# Hace que la ventana se ajuste al contenido
ventana.update_idletasks()
ventana.minsize(ventana.winfo_width(), ventana.winfo_height())

ventana.mainloop()