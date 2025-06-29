import tkinter as tk
from tkinter import ttk

class GUIComponents:
    """Clase para componentes de interfaz reutilizables"""
    
    # Configuración de colores y fuentes
    COLOR_FONDO = "#2E2E2E"
    BOTON_COLOR_BG = "#4CAF50"
    BOTON_COLOR_FG = "white"
    BOTON_ACTIVO = "#45a049"
    
    # Fuentes consistentes
    FUENTE_TITULO = ("Arial", 24, "bold")
    FUENTE_SUBTITULO = ("Arial", 20, "bold")
    FUENTE_NORMAL = ("Arial", 12)
    FUENTE_BOTON = ("Arial", 12, "bold")
    FUENTE_ENTRADA = ("Arial", 12)
    FUENTE_TEXTO = ("Arial", 11)
    
    @classmethod
    def crear_boton(cls, parent, texto, comando, width=18, height=2, **kwargs):
        """Crea un botón con estilo consistente"""
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=cls.BOTON_COLOR_BG,
            fg=cls.BOTON_COLOR_FG,
            font=cls.FUENTE_BOTON,
            width=width,
            height=height,
            activebackground=cls.BOTON_ACTIVO,
            relief="raised",
            bd=3,
            highlightthickness=0,
            **kwargs
        )
    
    @classmethod
    def crear_entrada(cls, parent, **kwargs):
        """Crea un campo de entrada con estilo consistente"""
        return tk.Entry(
            parent,
            font=cls.FUENTE_ENTRADA,
            **kwargs
        )
    
    @classmethod
    def crear_texto(cls, parent, **kwargs):
        """Crea un área de texto con estilo consistente"""
        return tk.Text(
            parent,
            font=cls.FUENTE_TEXTO,
            **kwargs
        )
    
    @classmethod
    def crear_lista(cls, parent, **kwargs):
        """Crea una lista con estilo consistente"""
        return tk.Listbox(
            parent,
            font=cls.FUENTE_NORMAL,
            **kwargs
        )
    
    @classmethod
    def crear_etiqueta(cls, parent, texto, font=None, fg="white", **kwargs):
        """Crea una etiqueta con estilo consistente"""
        if font is None:
            font = cls.FUENTE_NORMAL
        
        return tk.Label(
            parent,
            text=texto,
            font=font,
            bg=cls.COLOR_FONDO,
            fg=fg,
            **kwargs
        )
    
    @classmethod
    def crear_frame_con_titulo(cls, parent, titulo, pady=10):
        """Crea un frame con título centrado"""
        frame = tk.Frame(parent, bg=cls.COLOR_FONDO)
        frame.pack(pady=pady)
        
        cls.crear_etiqueta(frame, titulo, cls.FUENTE_SUBTITULO).pack()
        
        return frame
    
    @classmethod
    def crear_reloj(cls, parent):
        """Crea un reloj en tiempo real"""
        reloj = cls.crear_etiqueta(
            parent, 
            "", 
            font=("Arial", 16)
        )
        reloj.place(x=10, y=10)
        return reloj
    
    @classmethod
    def crear_lista_con_scrollbar(cls, parent, width=50, height=6):
        """Crea una lista con scrollbar"""
        frame_lista = tk.Frame(parent, bg=cls.COLOR_FONDO)
        frame_lista.pack(pady=5)
        
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        lista = cls.crear_lista(
            frame_lista,
            yscrollcommand=scrollbar.set,
            width=width,
            height=height
        )
        lista.pack(side=tk.LEFT)
        
        scrollbar.config(command=lista.yview)
        
        return lista, frame_lista
    
    @classmethod
    def crear_campo_anotaciones(cls, parent, titulo="Anotaciones durante el estudio:", width=60, height=5):
        """Crea un campo de anotaciones con título"""
        frame = tk.Frame(parent, bg=cls.COLOR_FONDO)
        frame.pack(pady=10)
        
        cls.crear_etiqueta(frame, titulo, cls.FUENTE_NORMAL).pack(pady=(0, 5))
        
        texto = cls.crear_texto(frame, width=width, height=height)
        texto.pack()
        
        return texto, frame 