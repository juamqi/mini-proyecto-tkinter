import tkinter as tk
from tkinter import ttk

class GUIComponents:
    COLOR_FONDO = "#2E2E2E"
    BOTON_COLOR_BG = "#4CAF50"
    BOTON_COLOR_FG = "white"
    BOTON_ACTIVO = "#45a049"
    
    FUENTE_TITULO = ("Arial", 24, "bold")
    FUENTE_SUBTITULO = ("Arial", 20, "bold")
    FUENTE_NORMAL = ("Arial", 12)
    FUENTE_BOTON = ("Arial", 12, "bold")
    FUENTE_ENTRADA = ("Arial", 12)
    FUENTE_TEXTO = ("Arial", 11)
    FUENTE_RELOJ = ("Arial", 14, "bold")
    
    @classmethod
    def crear_boton(cls, parent, texto, comando, width=18, height=2, **kwargs):
        btn = tk.Button(
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
            cursor="hand2",
            **kwargs
        )
        def on_enter(e): btn['background'] = cls.BOTON_ACTIVO
        def on_leave(e): btn['background'] = cls.BOTON_COLOR_BG
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn
    
    @classmethod
    def crear_entrada(cls, parent, **kwargs):
        entrada = tk.Entry(
            parent,
            font=cls.FUENTE_ENTRADA,
            bg="white",
            fg="black",
            insertbackground="black",
            relief="solid",
            bd=1,
            **kwargs
        )
        return entrada

    @classmethod
    def crear_lista_con_scrollbar(cls, parent, width, height):
        frame = tk.Frame(parent, bg=cls.COLOR_FONDO)
        listbox = tk.Listbox(
            frame,
            width=width,
            height=height,
            font=cls.FUENTE_NORMAL,
            bg="white",
            fg="black",
            selectbackground="#4CAF50",
            selectforeground="white"
        )
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        frame.pack(pady=5, fill="both", expand=True)
        return listbox, frame

    @classmethod
    def crear_etiqueta(cls, parent, texto, fuente, fg="white", **kwargs):
        return tk.Label(parent, text=texto, font=fuente, bg=cls.COLOR_FONDO, fg=fg, **kwargs)

    @classmethod
    def crear_texto(cls, parent, width, height):
        frame = tk.Frame(parent, bg="white", bd=1, relief="solid")
        text = tk.Text(
            frame,
            width=width,
            height=height,
            font=cls.FUENTE_TEXTO,
            wrap="word",
            relief="flat",
            padx=5,
            pady=5
        )
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.config(yscrollcommand=scrollbar.set)
        text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        frame.pack()
        return text

    @classmethod
    def crear_reloj(cls, parent):
        reloj = tk.Label(
            parent,
            text="Hora actual: --:--:--",
            font=cls.FUENTE_RELOJ,
            bg=cls.COLOR_FONDO,
            fg="#4CAF50",
            anchor="ne"
        )
        reloj.place(relx=0.98, rely=0.02, anchor="ne")
        return reloj