import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime

from database import DatabaseManager
from pomodoro_timer import PomodoroTimer
from gui_components import GUIComponents

class PomodoroApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("App de estudio con método Pomodoro")
        
        # Configurar pantalla completa
        self.ventana.state('zoomed')  # Para Windows
        # Alternativa para otros sistemas: self.ventana.attributes('-fullscreen', True)
        
        self.ventana.config(bg=GUIComponents.COLOR_FONDO)
        
        # Inicializar base de datos
        self.db = DatabaseManager()
        
        # Variables de control
        self.tema_actual = ""
        self.temporizador = None
        
        # Crear frames
        self.crear_frames()
        
        # Crear componentes
        self.crear_reloj()
        self.crear_menu_principal()
        self.crear_pantalla_estudio()
        self.crear_pantalla_estudiados()
        
        # Mostrar menú principal
        self.mostrar_frame(self.frame_inicio)
        
        # Iniciar reloj
        self.actualizar_reloj()
    
    def crear_frames(self):
        """Crea los frames principales de la aplicación"""
        self.frame_inicio = tk.Frame(self.ventana, bg=GUIComponents.COLOR_FONDO)
        self.frame_estudio = tk.Frame(self.ventana, bg=GUIComponents.COLOR_FONDO)
        self.frame_estudiados = tk.Frame(self.ventana, bg=GUIComponents.COLOR_FONDO)
        
        for frame in (self.frame_inicio, self.frame_estudio, self.frame_estudiados):
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    def crear_reloj(self):
        """Crea el reloj en tiempo real"""
        self.reloj = GUIComponents.crear_reloj(self.ventana)
    
    def actualizar_reloj(self):
        """Actualiza el reloj cada segundo"""
        self.reloj.config(text="Hora actual: " + time.strftime("%H:%M:%S"))
        self.ventana.after(1000, self.actualizar_reloj)
    
    def mostrar_frame(self, frame):
        """Muestra el frame especificado"""
        frame.tkraise()
    
    def crear_menu_principal(self):
        """Crea la pantalla del menú principal"""
        # Título
        GUIComponents.crear_etiqueta(
            self.frame_inicio, 
            "Menú Principal", 
            GUIComponents.FUENTE_TITULO
        ).pack(pady=20)
        
        # Explicación del método Pomodoro
        explicacion = (
            "El método Pomodoro consiste en trabajar durante 25 minutos sin distracciones,\n"
            "seguido por un descanso corto de 5 minutos. Cada 4 ciclos se realiza un descanso largo de 15 minutos.\n"
            "Este sistema ayuda a mantener la concentración y mejora la productividad."
        )
        GUIComponents.crear_etiqueta(
            self.frame_inicio, 
            explicacion, 
            GUIComponents.FUENTE_TEXTO,
            fg="lightgray",
            justify="center"
        ).pack(pady=10)
        
        # Botones de navegación
        GUIComponents.crear_boton(
            self.frame_inicio, 
            "Ir a Estudiar Temas", 
            lambda: self.mostrar_frame(self.frame_estudio),
            width=25, height=2
        ).pack(pady=20)
        
        GUIComponents.crear_boton(
            self.frame_inicio, 
            "Ver Temas Estudiados", 
            lambda: self.mostrar_frame(self.frame_estudiados),
            width=25, height=2
        ).pack(pady=10)
    
    def crear_pantalla_estudio(self):
        """Crea la pantalla de estudio con temporizador"""
        # Título
        GUIComponents.crear_etiqueta(
            self.frame_estudio, 
            "Estudiar Temas", 
            GUIComponents.FUENTE_SUBTITULO
        ).pack(pady=10)
        
        # Temporizador Pomodoro (asegúrate de que esté arriba y visible)
        self.temporizador_pomodoro = PomodoroTimer(self.frame_estudio, GUIComponents.COLOR_FONDO)
        # Padding extra para separar el temporizador del resto
        tk.Frame(self.frame_estudio, height=20, bg=GUIComponents.COLOR_FONDO).pack()
        
        # Sección de temas a estudiar
        frame_temas = tk.Frame(self.frame_estudio, bg=GUIComponents.COLOR_FONDO)
        frame_temas.pack(pady=10)
        
        GUIComponents.crear_etiqueta(
            frame_temas, 
            "Temas a Estudiar", 
            GUIComponents.FUENTE_NORMAL
        ).pack()
        
        # Campo para agregar temas
        self.entrada_tema_estudio = GUIComponents.crear_entrada(frame_temas, width=40)
        self.entrada_tema_estudio.pack(pady=5)
        
        # Lista de temas
        self.lista_temas_estudio, _ = GUIComponents.crear_lista_con_scrollbar(
            frame_temas, width=50, height=6
        )
        
        # Cargar temas pendientes
        self.cargar_temas_pendientes_lista(self.lista_temas_estudio)
        
        # Vincular evento de doble clic para seleccionar tema
        self.lista_temas_estudio.bind("<Double-Button-1>", self.seleccionar_tema_estudio)
        
        # Frame para botones de gestión
        frame_botones_estudio = tk.Frame(frame_temas, bg=GUIComponents.COLOR_FONDO)
        frame_botones_estudio.pack(pady=5)
        
        GUIComponents.crear_boton(
            frame_botones_estudio, 
            "Agregar tema", 
            self.agregar_tema_estudio,
            width=12, height=1
        ).pack(side="left", padx=5)
        
        GUIComponents.crear_boton(
            frame_botones_estudio, 
            "Eliminar tema", 
            self.eliminar_tema_estudio,
            width=12, height=1
        ).pack(side="left", padx=5)
        
        GUIComponents.crear_boton(
            frame_botones_estudio, 
            "Finalizar tema", 
            self.finalizar_tema_estudio,
            width=12, height=1
        ).pack(side="left", padx=5)
        
        # Campo de anotaciones durante el estudio
        self.anotaciones_estudio, _ = GUIComponents.crear_campo_anotaciones(
            self.frame_estudio, 
            "Anotaciones durante el estudio:",
            width=60, height=5
        )
        
        # Botón para volver al menú
        GUIComponents.crear_boton(
            self.frame_estudio, 
            "Volver al Menú", 
            lambda: self.mostrar_frame(self.frame_inicio),
            width=15, height=1
        ).pack(pady=10)
    
    def crear_pantalla_estudiados(self):
        """Crea la pantalla de temas estudiados"""
        # Título
        GUIComponents.crear_etiqueta(
            self.frame_estudiados, 
            "Temas Estudiados", 
            GUIComponents.FUENTE_SUBTITULO
        ).pack(pady=10)
        
        # Lista de temas estudiados
        self.lista_estudiados, _ = GUIComponents.crear_lista_con_scrollbar(
            self.frame_estudiados, width=60, height=8
        )
        
        # Cargar temas estudiados
        self.cargar_temas_estudiados()
        
        # Campo de anotaciones
        self.anotaciones_estudiados, _ = GUIComponents.crear_campo_anotaciones(
            self.frame_estudiados, 
            "Anotaciones del tema seleccionado:",
            width=60, height=8
        )
        
        # Frame para botones
        frame_botones_estudiados = tk.Frame(self.frame_estudiados, bg=GUIComponents.COLOR_FONDO)
        frame_botones_estudiados.pack(pady=10)
        
        GUIComponents.crear_boton(
            frame_botones_estudiados, 
            "Guardar anotación", 
            self.guardar_anotacion_estudiado,
            width=15, height=1
        ).pack(side="left", padx=5)
        
        GUIComponents.crear_boton(
            frame_botones_estudiados, 
            "Eliminar tema", 
            self.eliminar_tema_estudiado,
            width=15, height=1
        ).pack(side="left", padx=5)
        
        GUIComponents.crear_boton(
            frame_botones_estudiados, 
            "Volver al Menú", 
            lambda: self.mostrar_frame(self.frame_inicio),
            width=15, height=1
        ).pack(side="left", padx=5)
        
        # Vincular evento de selección
        self.lista_estudiados.bind("<<ListboxSelect>>", self.mostrar_anotacion_estudiado)
    
    def cargar_temas_pendientes_lista(self, lista):
        """Carga los temas pendientes en una lista específica"""
        lista.delete(0, tk.END)
        temas = self.db.obtener_temas_pendientes()
        for tema in temas:
            lista.insert(tk.END, tema)
    
    def cargar_temas_estudiados(self):
        """Carga los temas estudiados en la lista"""
        self.lista_estudiados.delete(0, tk.END)
        temas = self.db.obtener_temas_estudiados()
        for tema_data in temas:
            tema, fecha, tiempo_total, pomodoros, completado, anotaciones = tema_data
            # Formatear la información del tema
            tiempo_str = f"{tiempo_total // 60}:{tiempo_total % 60:02d}" if tiempo_total else "0:00"
            estado = "✓" if completado else "⚠"
            tema_formateado = f"{estado} {tema} - {fecha[:10]} - {tiempo_str} - {pomodoros} pomodoros"
            self.lista_estudiados.insert(tk.END, tema_formateado)
    
    def seleccionar_tema_estudio(self, event):
        """Selecciona un tema para estudiar y comienza el temporizador automáticamente"""
        seleccion = self.lista_temas_estudio.curselection()
        if seleccion:
            tema = self.lista_temas_estudio.get(seleccion)
            self.temporizador_pomodoro.establecer_tema(tema)
            self.temporizador_pomodoro.iniciar_temporizador(tema)
            messagebox.showinfo("Pomodoro iniciado", f"Tema '{tema}' seleccionado. El Pomodoro ha comenzado.")
    
    def agregar_tema_estudio(self):
        """Agrega un tema desde la pantalla de estudio"""
        tema = self.entrada_tema_estudio.get().strip()
        if tema:
            self.db.agregar_tema_pendiente(tema)
            self.entrada_tema_estudio.delete(0, tk.END)
            self.cargar_temas_pendientes_lista(self.lista_temas_estudio)
            # Establecer automáticamente el tema agregado como seleccionado
            self.temporizador_pomodoro.establecer_tema(tema)
            messagebox.showinfo("Tema agregado", f"Tema '{tema}' agregado y seleccionado. Puedes iniciar el Pomodoro.")
    
    def eliminar_tema_estudio(self):
        """Elimina un tema desde la pantalla de estudio"""
        seleccion = self.lista_temas_estudio.curselection()
        if seleccion:
            tema = self.lista_temas_estudio.get(seleccion)
            self.db.eliminar_tema_pendiente(tema)
            self.cargar_temas_pendientes_lista(self.lista_temas_estudio)
    
    def finalizar_tema_estudio(self):
        """Finaliza un tema y lo mueve a estudiados"""
        seleccion = self.lista_temas_estudio.curselection()
        if seleccion:
            tema = self.lista_temas_estudio.get(seleccion)
            anotaciones = self.anotaciones_estudio.get("1.0", tk.END).strip()
            
            # Obtener estadísticas del temporizador
            stats = self.temporizador_pomodoro.finalizar_estudio()
            
            # Finalizar tema en la base de datos
            self.db.finalizar_tema(
                tema=tema,
                tiempo_total=int(stats['tiempo_total_estudiado']),
                pomodoros_completados=stats['pomodoros_completados'],
                completado_pomodoro=stats['pomodoros_completados'] > 0,
                anotaciones=anotaciones
            )
            
            # Limpiar anotaciones
            self.anotaciones_estudio.delete("1.0", tk.END)
            
            # Actualizar listas
            self.cargar_temas_pendientes_lista(self.lista_temas_estudio)
            self.cargar_temas_estudiados()
            
            messagebox.showinfo("Tema finalizado", f"El tema '{tema}' ha sido marcado como estudiado.")
    
    def mostrar_anotacion_estudiado(self, event):
        """Muestra las anotaciones del tema seleccionado"""
        seleccion = self.lista_estudiados.curselection()
        if seleccion:
            tema_completo = self.lista_estudiados.get(seleccion)
            # Extraer solo el nombre del tema (sin el formato)
            tema = tema_completo.split(" - ")[0][2:]  # Remover el símbolo de estado
            
            # Obtener anotaciones de la base de datos
            temas = self.db.obtener_temas_estudiados()
            for tema_data in temas:
                if tema_data[0] == tema:
                    anotaciones = tema_data[5] or ""
                    self.anotaciones_estudiados.delete("1.0", tk.END)
                    self.anotaciones_estudiados.insert(tk.END, anotaciones)
                    break
    
    def guardar_anotacion_estudiado(self):
        """Guarda las anotaciones del tema seleccionado"""
        seleccion = self.lista_estudiados.curselection()
        if seleccion:
            tema_completo = self.lista_estudiados.get(seleccion)
            tema = tema_completo.split(" - ")[0][2:]  # Remover el símbolo de estado
            
            anotaciones = self.anotaciones_estudiados.get("1.0", tk.END).strip()
            self.db.actualizar_anotaciones(tema, anotaciones)
            
            messagebox.showinfo("Guardado", f"Anotaciones para '{tema}' guardadas correctamente.")
    
    def eliminar_tema_estudiado(self):
        """Elimina un tema de la lista de estudiados"""
        seleccion = self.lista_estudiados.curselection()
        if seleccion:
            tema_completo = self.lista_estudiados.get(seleccion)
            tema = tema_completo.split(" - ")[0][2:]  # Remover el símbolo de estado
            
            if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar '{tema}'?"):
                self.db.eliminar_tema_estudiado(tema)
                self.cargar_temas_estudiados()
                self.anotaciones_estudiados.delete("1.0", tk.END)
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        self.ventana.mainloop()

if __name__ == "__main__":
    app = PomodoroApp()
    app.ejecutar() 