import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="pomodoro_app.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temas_estudiados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tema TEXT NOT NULL,
                fecha_estudio TEXT NOT NULL,
                tiempo_total INTEGER DEFAULT 0,
                pomodoros_completados INTEGER DEFAULT 0,
                completado_pomodoro BOOLEAN DEFAULT 0,
                anotaciones TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temas_pendientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tema TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def agregar_tema_pendiente(self, tema):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO temas_pendientes (tema) VALUES (?)", (tema,))
        conn.commit()
        conn.close()
    
    def obtener_temas_pendientes(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT tema FROM temas_pendientes ORDER BY created_at")
        temas = [row[0] for row in cursor.fetchall()]
        conn.close()
        return temas
    
    def eliminar_tema_pendiente(self, tema):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM temas_pendientes WHERE tema = ?", (tema,))
        conn.commit()
        conn.close()
    
    def finalizar_tema(self, tema, tiempo_total=0, pomodoros_completados=0, 
                      completado_pomodoro=True, anotaciones=""):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        fecha_estudio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO temas_estudiados 
            (tema, fecha_estudio, tiempo_total, pomodoros_completados, completado_pomodoro, anotaciones)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (tema, fecha_estudio, tiempo_total, pomodoros_completados, completado_pomodoro, anotaciones))
        
        cursor.execute("DELETE FROM temas_pendientes WHERE tema = ?", (tema,))
        
        conn.commit()
        conn.close()
    
    def obtener_temas_estudiados(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT tema, fecha_estudio, tiempo_total, pomodoros_completados, 
                   completado_pomodoro, anotaciones 
            FROM temas_estudiados 
            ORDER BY fecha_estudio DESC
        ''')
        temas = cursor.fetchall()
        conn.close()
        return temas
    
    def actualizar_anotaciones(self, tema, anotaciones):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE temas_estudiados SET anotaciones = ? WHERE tema = ?", (anotaciones, tema))
        conn.commit()
        conn.close()
    
    def eliminar_tema_estudiado(self, tema):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM temas_estudiados WHERE tema = ?", (tema,))
        conn.commit()
        conn.close() 