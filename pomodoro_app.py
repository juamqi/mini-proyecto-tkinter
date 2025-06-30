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
        self.ventana.state('zoomed')  
        self.ventana.config(bg=GUIComponents.COLOR_FONDO)
        self.db = DatabaseManager()
        self.tema_actual = ""
        self.temporizador = None
        self.crear_frames()
        self.crear_reloj()
        self.crear_menu_barra()
        self.crear_pantalla_bienvenida()
        self.crear_menu_principal()
        self.crear_pantalla_estudio()
        self.crear_pantalla_estudiados()
        self.mostrar_frame(self.frame_bienvenida)
        self.actualizar_reloj()
    
    def crear_frames(self):
        self.frame_bienvenida = tk.Frame(self.ventana, bg=GUIComponents.COLOR_FONDO)
        self.frame_inicio = tk.Frame(self.ventana, bg=GUIComponents.COLOR_FONDO)
        self.frame_estudio = tk.Frame(self.ventana, bg=GUIComponents.COLOR_FONDO)
        self.frame_estudiados = tk.Frame(self.ventana, bg=GUIComponents.COLOR_FONDO)

        for frame in (self.frame_bienvenida, self.frame_inicio, self.frame_estudio, self.frame_estudiados):
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    def crear_menu_barra(self):
        menubar = tk.Menu(self.ventana)
        self.ventana.config(menu=menubar)
        menu_principal = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menú", menu=menu_principal)
        menu_principal.add_command(label="Cómo usar", command=lambda: self.mostrar_frame(self.frame_bienvenida))
        menu_principal.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        menu_principal.add_separator()
        menu_principal.add_command(label="Salir", command=self.ventana.quit)
    
    def mostrar_acerca_de(self):
        messagebox.showinfo(
            "Acerca de",
            "App de Estudio Pomodoro v1.0\n\n"
            "Desarrollada con Python y tkinter para el curso de Desarrollo Web\n"
            "Informatorio Chaco - 2025\n\n"
            "Integrantes del grupo 7:\n" 
            "- CANTEROS, Tomás Ezequiel\n"
            "- KASS, Juan Pablo Miguel\n"
            "- LEPRERI, Javier Guillermo\n"
            "- MARTINETTI, Melisa\n"
            "- MEDINA DURAN, José Ignacio\n\n"
            "Método Pomodoro para mejorar tu productividad"
        )
    
    def crear_reloj(self):
        self.reloj = GUIComponents.crear_reloj(self.ventana)
    
    def actualizar_reloj(self):
        self.reloj.config(text="Hora actual: " + time.strftime("%H:%M:%S"))
        self.ventana.after(1000, self.actualizar_reloj)
    
    def mostrar_frame(self, frame):
        frame.tkraise()
    
    def crear_pantalla_bienvenida(self):
        contenedor = tk.Frame(self.frame_bienvenida, bg=GUIComponents.COLOR_FONDO)
        contenedor.place(relx=0.5, rely=0.5, anchor="center")
        
        GUIComponents.crear_etiqueta(
            contenedor,
            "¡Bienvenido a tu App de Estudio Pomodoro!",
            GUIComponents.FUENTE_TITULO,
            fg="#4CAF50"
        ).pack(pady=20)
        
        frame_contenido = tk.Frame(contenedor, bg=GUIComponents.COLOR_FONDO, padx=40, pady=20)
        frame_contenido.pack()
        
        texto_herramienta = (
            "Esta herramienta te ayudará a gestionar tus sesiones de estudio\n"
            "de manera eficiente utilizando el método Pomodoro."
        )
        GUIComponents.crear_etiqueta(
            frame_contenido,
            texto_herramienta,
            GUIComponents.FUENTE_NORMAL,
            fg="white"
        ).pack(pady=10)
        
        GUIComponents.crear_etiqueta(
            frame_contenido,
            "¿Cómo funciona el método Pomodoro?",
            ("Arial", 14, "bold"),
            fg="#4CAF50"
        ).pack(pady=(20, 10))
        
        explicacion_pomodoro = (
            "• 25 minutos de estudio concentrado\n"
            "• 5 minutos de descanso corto\n"
            "• Cada 4 pomodoros: 15 minutos de descanso largo\n\n"
            "Este sistema mejora tu concentración y productividad"
        )
        GUIComponents.crear_etiqueta(
            frame_contenido,
            explicacion_pomodoro,
            GUIComponents.FUENTE_NORMAL,
            fg="lightgray",
            justify="left"
        ).pack(pady=10)
        
        # Instrucciones de uso
        GUIComponents.crear_etiqueta(
            frame_contenido,
            "¿Cómo usar la aplicación?",
            ("Arial", 14, "bold"),
            fg="#4CAF50"
        ).pack(pady=(20, 10))
        
        instrucciones = (
            "1. Agrega temas escribiendo en el campo y presionando 'Agregar'\n"
            "2. Haz clic en cualquier tema para seleccionarlo\n"
            "3. Presiona 'Iniciar' en la sección de Pomodoro para comenzar el temporizador\n"
            "4. Toma notas mientras estudias en el área de anotaciones\n"
            "5. Al finalizar, marca el tema como 'Completado'"
        )
        GUIComponents.crear_etiqueta(
            frame_contenido,
            instrucciones,
            GUIComponents.FUENTE_NORMAL,
            fg="lightblue",
            justify="left"
        ).pack(pady=10)
        
        GUIComponents.crear_boton(
            contenedor,
            "¡Entendido!",
            lambda: self.mostrar_frame(self.frame_inicio),
            width=20,
            height=2
        ).pack(pady=30)
    
    def crear_menu_principal(self):
        contenedor = tk.Frame(self.frame_inicio, bg=GUIComponents.COLOR_FONDO)
        contenedor.place(relx=0.5, rely=0.5, anchor="center")
        
        GUIComponents.crear_etiqueta(
            contenedor, 
            "Menú Principal", 
            GUIComponents.FUENTE_TITULO,
            fg="#4CAF50"
        ).pack(pady=30)
        
        frame_botones = tk.Frame(contenedor, bg=GUIComponents.COLOR_FONDO)
        frame_botones.pack(pady=20)
        
        btn_estudiar = GUIComponents.crear_boton(
            frame_botones, 
            "Ir a Estudiar Temas", 
            lambda: self.mostrar_frame(self.frame_estudio),
            width=25, 
            height=3
        )
        btn_estudiar.config(font=("Arial", 14, "bold"))
        btn_estudiar.pack(pady=15)
        
        btn_historial = GUIComponents.crear_boton(
            frame_botones, 
            "Historial de Temas", 
            lambda: [self.mostrar_frame(self.frame_estudiados), self.cargar_temas_estudiados()],
            width=25, 
            height=3
        )
        btn_historial.config(font=("Arial", 14, "bold"))
        btn_historial.pack(pady=15)
        
        tip = "Tip: Mantén tu espacio de estudio ordenado y libre de distracciones"
        GUIComponents.crear_etiqueta(
            contenedor,
            tip,
            GUIComponents.FUENTE_NORMAL,
            fg="lightblue"
        ).pack(pady=30)
    
    def crear_pantalla_estudio(self):
        canvas = tk.Canvas(self.frame_estudio, bg=GUIComponents.COLOR_FONDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame_estudio, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=GUIComponents.COLOR_FONDO)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        contenedor_principal = tk.Frame(scrollable_frame, bg=GUIComponents.COLOR_FONDO)
        contenedor_principal.pack(expand=True, fill="both", padx=50, pady=20)
        
        GUIComponents.crear_etiqueta(
            contenedor_principal, 
            "Estudiar Temas", 
            GUIComponents.FUENTE_TITULO,
            fg="#4CAF50"
        ).pack(pady=(0, 30))
        
        frame_gestion = tk.LabelFrame(
            contenedor_principal, 
            text="Gestión de Temas", 
            font=("Arial", 14, "bold"),
            bg=GUIComponents.COLOR_FONDO,
            fg="white",
            bd=2,
            relief="groove"
        )
        frame_gestion.pack(fill="x", pady=(0, 20), padx=10, ipady=10)
        
        GUIComponents.crear_etiqueta(
            frame_gestion,
            "Escribe un tema, presiona 'Agregar', luego haz clic en cualquier tema para seleccionarlo.",
            ("Arial", 11),
            fg="lightblue"
        ).pack(pady=(5, 15))
        
        frame_agregar = tk.Frame(frame_gestion, bg=GUIComponents.COLOR_FONDO)
        frame_agregar.pack(pady=(0, 10))
        
        GUIComponents.crear_etiqueta(
            frame_agregar,
            "Nuevo tema:",
            ("Arial", 12, "bold"),
            fg="white"
        ).pack(side="left", padx=(0, 10))
        
        self.entrada_tema_estudio = GUIComponents.crear_entrada(frame_agregar, width=40)
        self.entrada_tema_estudio.pack(side="left", padx=(0, 10))
        
        self.entrada_tema_estudio.bind("<Return>", lambda e: self.agregar_tema_estudio())
        
        btn_agregar = GUIComponents.crear_boton(
            frame_agregar, 
            "➕ Agregar", 
            self.agregar_tema_estudio,
            width=12, height=1
        )
        btn_agregar.pack(side="left")
        
        GUIComponents.crear_etiqueta(
            frame_gestion,
            "Temas pendientes (haz clic para seleccionar):",
            ("Arial", 12, "bold"),
            fg="white"
        ).pack(pady=(20, 5), anchor="w")
        
        frame_lista = tk.Frame(frame_gestion, bg="white", bd=2, relief="sunken")
        frame_lista.pack(fill="x", pady=(0, 10))
        
        self.lista_temas_estudio = tk.Listbox(
            frame_lista,
            height=6,  
            font=GUIComponents.FUENTE_NORMAL,
            bg="white",
            fg="black",
            selectbackground="#4CAF50",
            selectforeground="white",
            activestyle="none"
        )
        
        scrollbar_lista = tk.Scrollbar(frame_lista, orient="vertical", command=self.lista_temas_estudio.yview)
        self.lista_temas_estudio.config(yscrollcommand=scrollbar_lista.set)
        
        self.lista_temas_estudio.pack(side="left", fill="both", expand=True)
        scrollbar_lista.pack(side="right", fill="y")
        
        self.cargar_temas_pendientes_lista(self.lista_temas_estudio)
        
        self.lista_temas_estudio.bind("<Button-1>", self.seleccionar_tema_estudio)
        self.lista_temas_estudio.bind("<<ListboxSelect>>", self.seleccionar_tema_estudio)
        
        self.etiqueta_tema_seleccionado = GUIComponents.crear_etiqueta(
            frame_gestion,
            "Tema seleccionado: Ninguno",
            ("Arial", 12, "bold"),
            fg="#FFE66D"
        )
        self.etiqueta_tema_seleccionado.pack(pady=10)
        
        frame_botones_gestion = tk.Frame(frame_gestion, bg=GUIComponents.COLOR_FONDO)
        frame_botones_gestion.pack(pady=10)
        
        GUIComponents.crear_boton(
            frame_botones_gestion, 
            "Eliminar", 
            self.eliminar_tema_estudio,
            width=15, height=1
        ).pack(side="left", padx=5)
        
        GUIComponents.crear_boton(
            frame_botones_gestion, 
            "Completado", 
            self.finalizar_tema_estudio,
            width=15, height=1
        ).pack(side="left", padx=5)
        
        frame_temporizador = tk.LabelFrame(
            contenedor_principal, 
            text="Temporizador Pomodoro", 
            font=("Arial", 14, "bold"),
            bg=GUIComponents.COLOR_FONDO,
            fg="white",
            bd=2,
            relief="groove"
        )
        frame_temporizador.pack(fill="x", pady=(0, 20), padx=10, ipady=10)
        
        GUIComponents.crear_etiqueta(
            frame_temporizador,
            "Selecciona un tema arriba y presiona 'Iniciar' para comenzar",
            ("Arial", 11),
            fg="lightblue"
        ).pack(pady=(5, 10))
        
        self.temporizador_pomodoro = PomodoroTimer(frame_temporizador, GUIComponents.COLOR_FONDO)
        
        frame_anotaciones = tk.LabelFrame(
            contenedor_principal, 
            text="Anotaciones de Estudio", 
            font=("Arial", 14, "bold"),
            bg=GUIComponents.COLOR_FONDO,
            fg="white",
            bd=2,
            relief="groove"
        )
        frame_anotaciones.pack(fill="x", pady=(0, 20), padx=10, ipady=10)
        
        GUIComponents.crear_etiqueta(
            frame_anotaciones,
            "Escribe aquí tus notas mientras estudias:",
            ("Arial", 11),
            fg="lightblue"
        ).pack(pady=(5, 10))
        
        frame_texto = tk.Frame(frame_anotaciones, bg="white", bd=2, relief="sunken")
        frame_texto.pack(fill="x", pady=(0, 10))
        
        self.anotaciones_estudio = tk.Text(
            frame_texto,
            height=6,  
            font=GUIComponents.FUENTE_TEXTO,
            wrap="word",
            relief="flat",
            padx=5,
            pady=5
        )
        
        scrollbar_notas = tk.Scrollbar(frame_texto, orient="vertical", command=self.anotaciones_estudio.yview)
        self.anotaciones_estudio.config(yscrollcommand=scrollbar_notas.set)
        
        self.anotaciones_estudio.pack(side="left", fill="both", expand=True)
        scrollbar_notas.pack(side="right", fill="y")
        
        GUIComponents.crear_boton(
            contenedor_principal, 
            "Volver al Menú", 
            lambda: self.mostrar_frame(self.frame_inicio),
            width=20, height=2
        ).pack(pady=30)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def crear_pantalla_estudiados(self):
        GUIComponents.crear_etiqueta(
            self.frame_estudiados, 
            "Historial de Temas Estudiados", 
            GUIComponents.FUENTE_SUBTITULO,
            fg="#4CAF50"
        ).pack(pady=20)
        
        contenedor = tk.Frame(self.frame_estudiados, bg=GUIComponents.COLOR_FONDO)
        contenedor.pack(expand=True, fill="both", padx=40)
        
        GUIComponents.crear_etiqueta(
            contenedor,
            "Sesiones completadas:",
            GUIComponents.FUENTE_NORMAL,
            fg="white"
        ).pack(pady=(0, 10))
        
        self.lista_estudiados, _ = GUIComponents.crear_lista_con_scrollbar(
            contenedor, width=80, height=10
        )
        
        frame_anotaciones = tk.Frame(contenedor, bg=GUIComponents.COLOR_FONDO)
        frame_anotaciones.pack(fill="both", expand=True, pady=20)
        
        GUIComponents.crear_etiqueta(
            frame_anotaciones,
            "Anotaciones del tema seleccionado:",
            GUIComponents.FUENTE_NORMAL,
            fg="white"
        ).pack(pady=(0, 5))
        
        self.anotaciones_estudiados = GUIComponents.crear_texto(
            frame_anotaciones,
            width=80,
            height=8
        )
        self.anotaciones_estudiados.pack()
        
        frame_botones_estudiados = tk.Frame(contenedor, bg=GUIComponents.COLOR_FONDO)
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
        
        self.lista_estudiados.bind("<<ListboxSelect>>", self.mostrar_anotacion_estudiado)
    
    def cargar_temas_pendientes_lista(self, lista):
        lista.delete(0, tk.END)
        temas = self.db.obtener_temas_pendientes()
        for tema in temas:
            lista.insert(tk.END, tema)
    
    def cargar_temas_estudiados(self):
        self.lista_estudiados.delete(0, tk.END)
        temas = self.db.obtener_temas_estudiados()
        for tema_data in temas:
            tema, fecha, tiempo_total, pomodoros, completado, anotaciones = tema_data
            tiempo_str = f"{tiempo_total // 60}:{tiempo_total % 60:02d}" if tiempo_total else "0:00"
            estado = "✓" if completado else "⚠"
            tema_formateado = f"{estado} {tema} - {fecha[:10]} - {tiempo_str} - {pomodoros} pomodoros"
            self.lista_estudiados.insert(tk.END, tema_formateado)
    
    def seleccionar_tema_estudio(self, event):
        seleccion = self.lista_temas_estudio.curselection()
        if seleccion:
            tema = self.lista_temas_estudio.get(seleccion)
            self.tema_actual = tema
            self.etiqueta_tema_seleccionado.config(text=f"Tema seleccionado: {tema}")
            self.temporizador_pomodoro.establecer_tema(tema)
            
    def agregar_tema_estudio(self):
        tema = self.entrada_tema_estudio.get().strip()
        if tema:
            self.db.agregar_tema_pendiente(tema)
            self.entrada_tema_estudio.delete(0, tk.END)
            self.cargar_temas_pendientes_lista(self.lista_temas_estudio)
            messagebox.showinfo("Tema agregado", f"¡Perfecto! El tema '{tema}' fue agregado a tu lista.\n\nHaz clic en él para seleccionarlo.")
        else:
            messagebox.showwarning("Campo vacío", "Por favor, escribe el nombre del tema antes de agregarlo.")
    
    def eliminar_tema_estudio(self):
        seleccion = self.lista_temas_estudio.curselection()
        if seleccion:
            tema = self.lista_temas_estudio.get(seleccion)
            if messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de eliminar '{tema}' de tu lista?"):
                self.db.eliminar_tema_pendiente(tema)
                self.cargar_temas_pendientes_lista(self.lista_temas_estudio)
                # Limpiar selección si era el tema eliminado
                if self.tema_actual == tema:
                    self.tema_actual = ""
                    self.etiqueta_tema_seleccionado.config(text="Tema seleccionado: Ninguno")
                    self.temporizador_pomodoro.establecer_tema("")
        else:
            messagebox.showwarning("Sin selección", "Por favor, selecciona un tema de la lista para eliminar.")
    
    def finalizar_tema_estudio(self):
        if not self.tema_actual:
            messagebox.showwarning("Sin tema seleccionado", "Por favor, selecciona un tema antes de marcarlo como completado.")
            return
            
        anotaciones = self.anotaciones_estudio.get("1.0", tk.END).strip()
        
        stats = self.temporizador_pomodoro.finalizar_estudio()
        
        self.db.finalizar_tema(
            tema=self.tema_actual,
            tiempo_total=int(stats['tiempo_total_estudiado']),
            pomodoros_completados=stats['pomodoros_completados'],
            completado_pomodoro=stats['pomodoros_completados'] > 0,
            anotaciones=anotaciones
        )
        
        self.anotaciones_estudio.delete("1.0", tk.END)
        self.tema_actual = ""
        self.etiqueta_tema_seleccionado.config(text="Tema seleccionado: Ninguno")
        
        self.cargar_temas_pendientes_lista(self.lista_temas_estudio)
        
        messagebox.showinfo(
            "¡Excelente trabajo!", 
            f"Has completado el tema.\n\n"
            f"Pomodoros completados: {stats['pomodoros_completados']}\n"
            f"Tiempo total: {int(stats['tiempo_total_estudiado'])//60} minutos\n\n"
            f"¡Sigue así!"
        )
    
    def mostrar_anotacion_estudiado(self, event):
        """Muestra las anotaciones del tema seleccionado"""
        seleccion = self.lista_estudiados.curselection()
        if seleccion:
            tema_completo = self.lista_estudiados.get(seleccion)
            tema = tema_completo.split(" - ")[0][2:] 
            
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
            tema = tema_completo.split(" - ")[0][2:]  
            
            anotaciones = self.anotaciones_estudiados.get("1.0", tk.END).strip()
            self.db.actualizar_anotaciones(tema, anotaciones)
            
            messagebox.showinfo("Guardado", f"Las anotaciones para '{tema}' fueron guardadas correctamente.")
    
    def eliminar_tema_estudiado(self):
        """Elimina un tema de la lista de estudiados"""
        seleccion = self.lista_estudiados.curselection()
        if seleccion:
            tema_completo = self.lista_estudiados.get(seleccion)
            tema = tema_completo.split(" - ")[0][2:] 
            
            if messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar '{tema}' del historial?"):
                self.db.eliminar_tema_estudiado(tema)
                self.cargar_temas_estudiados()
                self.anotaciones_estudiados.delete("1.0", tk.END)
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        self.ventana.mainloop()

if __name__ == "__main__":
    app = PomodoroApp()
    app.ejecutar()