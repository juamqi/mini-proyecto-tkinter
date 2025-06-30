import tkinter as tk
from tkinter import messagebox
import math
import time
import random

class PomodoroTimer:
    def __init__(self, parent_frame, color_fondo):
        self.parent_frame = parent_frame
        self.color_fondo = color_fondo
        
        # Variables del temporizador
        self.repeticiones = 0
        self.temporizador = None
        self.tiempo_restante = 0
        self.tema_actual = ""
        self.tiempo_inicio = 0
        self.tiempo_total_estudiado = 0
        self.estudio_iniciado = False
        self.pausado = False
        
        # Configuración de tiempos
        self.tiempo_trabajo = 25 * 60  # 25 minutos
        self.descanso_corto = 5 * 60   # 5 minutos
        self.descanso_largo = 15 * 60  # 15 minutos
        
        # Configuración visual
        self.BOTON_COLOR_BG = "#4CAF50"
        self.BOTON_COLOR_FG = "white"
        self.BOTON_FONT = ("Arial", 12, "bold")
        self.BOTON_ANCHO = 15
        self.BOTON_ALTO = 2
        self.BOTON_ACTIVO = "#45a049"
        
        # Frases motivacionales
        self.frases_trabajo = [
            "¡Excelente trabajo! 💪 Tómate un respiro.",
            "¡Lo lograste! 🎯 Es hora de descansar.",
            "¡Sesión completada! 🌟 Te lo has ganado.",
            "¡Increíble concentración! 🧠 Ahora relájate.",
            "¡Objetivo cumplido! ✅ Tiempo de recargar energías.",
            "¡Eres imparable! 🚀 Disfruta tu descanso.",
            "¡Gran esfuerzo! 💯 Te mereces un break.",
            "¡Productividad al máximo! ⚡ Hora de relajarse."
        ]
        
        self.frases_descanso = [
            "¡Descanso terminado! 🔥 ¡A por el siguiente!",
            "¡Energías renovadas! 💪 ¡Vamos con todo!",
            "¡Listo para continuar! 🎯 ¡Tú puedes!",
            "¡Recargado al 100%! ⚡ ¡Sigamos estudiando!",
            "¡De vuelta a la acción! 🚀 ¡Enfócate!",
            "¡Mente fresca! 🧠 ¡A conquistar ese tema!",
            "¡Preparado para brillar! ✨ ¡Adelante!",
            "¡Como nuevo! 🌟 ¡Continuemos aprendiendo!"
        ]
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz del temporizador"""
        # Contenedor principal
        self.contenedor = tk.Frame(self.parent_frame, bg=self.color_fondo)
        self.contenedor.pack(pady=20)
        
        # Título del temporizador
        self.etiqueta_titulo = tk.Label(
            self.contenedor, 
            text="Temporizador Pomodoro", 
            font=("Arial", 28, "bold"), 
            bg=self.color_fondo, 
            fg="white"
        )
        self.etiqueta_titulo.pack(pady=10)
        
        # Display del tiempo
        self.etiqueta_tiempo = tk.Label(
            self.contenedor, 
            text="25:00", 
            font=("Arial", 48, "bold"), 
            bg=self.color_fondo, 
            fg="white"
        )
        self.etiqueta_tiempo.pack(pady=10)
        
        # Tema actual
        self.etiqueta_tema_estudio = tk.Label(
            self.contenedor, 
            text="Tema: Ninguno seleccionado", 
            font=("Arial", 14), 
            bg=self.color_fondo, 
            fg="lightblue"
        )
        self.etiqueta_tema_estudio.pack(pady=5)
        
        # Marcas de sesiones completadas
        self.etiqueta_marcas = tk.Label(
            self.contenedor, 
            font=("Arial", 20), 
            bg=self.color_fondo, 
            fg="#4CAF50"
        )
        self.etiqueta_marcas.pack(pady=10)
        
        # Frame para los botones
        frame_botones = tk.Frame(self.contenedor, bg=self.color_fondo)
        frame_botones.pack(pady=10)
        
        # Botón de iniciar
        self.boton_iniciar = self.crear_boton("Iniciar", self.iniciar_temporizador)
        self.boton_iniciar.pack(side="left", padx=5)
        
        # Botón de pausar/reanudar
        self.boton_pausar = self.crear_boton("Pausar", self.pausar_reanudar)
        self.boton_pausar.pack(side="left", padx=5)
        self.boton_pausar.config(state="disabled")
        
        # Botón de reiniciar
        self.boton_reiniciar = self.crear_boton("Reiniciar", self.reiniciar_temporizador)
        self.boton_reiniciar.pack(side="left", padx=5)
    
    def crear_boton(self, texto, comando):
        """Crea un botón con estilo consistente"""
        return tk.Button(
            self.contenedor,
            text=texto,
            command=comando,
            bg=self.BOTON_COLOR_BG,
            fg=self.BOTON_COLOR_FG,
            font=self.BOTON_FONT,
            width=self.BOTON_ANCHO,
            height=self.BOTON_ALTO,
            activebackground=self.BOTON_ACTIVO,
            relief="raised",
            bd=3,
            highlightthickness=0
        )
    
    def iniciar_temporizador(self, tema_seleccionado=None):
        """Inicia el temporizador Pomodoro"""
        if tema_seleccionado:
            self.tema_actual = tema_seleccionado
            self.etiqueta_tema_estudio.config(text=f"Tema: {self.tema_actual}")
        
        if not self.tema_actual:
            messagebox.showwarning("Selecciona un tema", "Por favor, selecciona un tema antes de iniciar el Pomodoro.")
            return
        
        self.estudio_iniciado = True
        self.pausado = False
        self.boton_iniciar.config(state="disabled")
        self.boton_pausar.config(state="normal")
        
        # Cancelar temporizador anterior si existe
        if self.temporizador:
            self.parent_frame.after_cancel(self.temporizador)
            self.temporizador = None
        
        self.repeticiones += 1
        self.tiempo_inicio = time.time()
        
        if self.repeticiones % 8 == 0:
            self.tiempo_restante = self.descanso_largo
            self.etiqueta_titulo.config(text="Descanso largo", fg="#FF6B6B")
        elif self.repeticiones % 2 == 0:
            self.tiempo_restante = self.descanso_corto
            self.etiqueta_titulo.config(text="Descanso corto", fg="#4ECDC4")
        else:
            self.tiempo_restante = self.tiempo_trabajo
            self.etiqueta_titulo.config(text="Tiempo de estudio", fg="#FFE66D")
        
        self.cuenta_regresiva(self.tiempo_restante)
    
    def pausar_reanudar(self):
        """Pausa o reanuda el temporizador"""
        if not self.pausado:
            # Pausar
            self.pausado = True
            self.boton_pausar.config(text="Reanudar")
            if self.temporizador:
                self.parent_frame.after_cancel(self.temporizador)
                self.temporizador = None
        else:
            # Reanudar
            self.pausado = False
            self.boton_pausar.config(text="Pausar")
            self.cuenta_regresiva(self.tiempo_restante)
    
    def cuenta_regresiva(self, tiempo):
        """Ejecuta la cuenta regresiva del temporizador"""
        if tiempo <= 0:
            # Sesión completada
            self.actualizar_marcas()
            
            # Calcular tiempo estudiado si es una sesión de trabajo
            if self.repeticiones % 2 == 1:  # Sesión de trabajo
                tiempo_sesion = time.time() - self.tiempo_inicio
                self.tiempo_total_estudiado += tiempo_sesion
                frase = random.choice(self.frases_trabajo)
                titulo = "¡Sesión de estudio completada!"
            elif self.repeticiones % 8 == 0:
                frase = random.choice(self.frases_descanso)
                titulo = "¡Descanso largo terminado!"
            else:
                frase = random.choice(self.frases_descanso)
                titulo = "¡Descanso terminado!"
            
            # Mostrar notificación con frase motivacional
            messagebox.showinfo(titulo, frase)
            
            # Habilitar botón de iniciar para continuar
            self.boton_iniciar.config(state="normal")
            self.boton_pausar.config(state="disabled", text="Pausar")
            
            return
        
        # Actualizar display
        minutos = math.floor(tiempo / 60)
        segundos = tiempo % 60
        tiempo_str = f"{minutos:02d}:{segundos:02d}"
        self.etiqueta_tiempo.config(text=tiempo_str)
        
        # Cambiar color según el tiempo restante
        if tiempo <= 60:  # Último minuto
            self.etiqueta_tiempo.config(fg="#FF6B6B")
        elif tiempo <= 300:  # Últimos 5 minutos
            self.etiqueta_tiempo.config(fg="#FFE66D")
        else:
            self.etiqueta_tiempo.config(fg="white")
        
        # Programar siguiente tick
        self.tiempo_restante = tiempo - 1
        self.temporizador = self.parent_frame.after(1000, self.cuenta_regresiva, self.tiempo_restante)
    
    def reiniciar_temporizador(self):
        """Reinicia el temporizador a su estado inicial"""
        if self.temporizador:
            self.parent_frame.after_cancel(self.temporizador)
            self.temporizador = None
        
        self.etiqueta_titulo.config(text="Temporizador Pomodoro", fg="white")
        self.etiqueta_tiempo.config(text="25:00", fg="white")
        self.etiqueta_marcas.config(text="")
        self.etiqueta_tema_estudio.config(text="Tema: Ninguno seleccionado")
        self.boton_iniciar.config(state="normal")
        self.boton_pausar.config(state="disabled", text="Pausar")
        self.repeticiones = 0
        self.tiempo_restante = 0
        self.tema_actual = ""
        self.tiempo_total_estudiado = 0
        self.tiempo_inicio = 0
        self.estudio_iniciado = False
        self.pausado = False
    
    def actualizar_marcas(self):
        """Actualiza las marcas de sesiones completadas"""
        sesiones_trabajo = math.floor(self.repeticiones / 2)
        marcas = "🍅" * sesiones_trabajo
        self.etiqueta_marcas.config(text=marcas)
    
    def obtener_estadisticas(self):
        """Retorna las estadísticas del temporizador"""
        return {
            'repeticiones': self.repeticiones,
            'tiempo_total_estudiado': self.tiempo_total_estudiado,
            'pomodoros_completados': math.floor(self.repeticiones / 2),
            'tema_actual': self.tema_actual
        }
    
    def finalizar_estudio(self):
        """Finaliza el estudio y retorna las estadísticas"""
        if self.temporizador:
            self.parent_frame.after_cancel(self.temporizador)
            self.temporizador = None
        
        # Si estaba en medio de una sesión de trabajo, contar el tiempo parcial
        if self.estudio_iniciado and self.repeticiones % 2 == 1:
            tiempo_parcial = time.time() - self.tiempo_inicio
            self.tiempo_total_estudiado += tiempo_parcial
        
        stats = self.obtener_estadisticas()
        
        # Reiniciar para el siguiente tema
        self.reiniciar_temporizador()
        
        return stats
    
    def establecer_tema(self, tema):
        """Establece el tema actual para el estudio"""
        self.tema_actual = tema
        self.etiqueta_tema_estudio.config(text=f"Tema: {self.tema_actual}")