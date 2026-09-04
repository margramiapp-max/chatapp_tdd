# database.py implementa la estructura inicial de la base de datos y las funciones para interactuar con ella.

import sqlite3

# Agrega el pragma directamente en la firma de la función
def inicializar_db(conn):
    """Crea la tabla de perfiles de usuario si no existe."""
    
    cursor = conn.cursor() 
    # ACTIVAR SOPORTE DE LLAVES FORÁNEAS EN SQLITE
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            biografia TEXT
        )
    """)
    conn.commit() # pragma: no cover

# --- C (Create) ---
def crear_usuario(conn, username, nombre, biografia):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (username, nombre, biografia) VALUES (?, ?, ?)",
        (username, nombre, biografia)
    )
    conn.commit()
    return cursor.lastrowid

# --- R (Read) ---
def obtener_usuario(conn, user_id):
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return dict(row) if row else None

# --- U (Update) --- (Añadir a database.py)
def actualizar_usuario(conn, user_id, nuevo_nombre, nueva_biografia):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET nombre = ?, biografia = ? WHERE id = ?",
        (nuevo_nombre, nueva_biografia, user_id)
    )
    conn.commit()

# --- D (Delete) --- (Añadir a database.py)
def eliminar_usuario(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE id = ?", (user_id,))
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()



# --- ACTUALIZACIÓN DE database.py ---
import sqlite3

def inicializar_db(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Tabla de usuarios intacta
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            biografia TEXT
        )
    """)
    
    # TABLA DE MENSAJES MEJORADA (Canales y One-to-One)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            remitente_id INTEGER NOT NULL,
            tipo_destino TEXT NOT NULL, -- "canal" o "privado"
            destino_id INTEGER NOT NULL,   -- Puede ser un ID de canal o el ID de otro usuario
            texto TEXT NOT NULL,
            fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (remitente_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    """)
    conn.commit()

# --- FUNCIONES DE MENSAJERÍA AVANZADA ---

def enviar_mensaje(conn, remitente_id, tipo_destino, destino_id, texto):
    """Guarda un mensaje especificando su origen, destino y tipo."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("""
        INSERT INTO mensajes (remitente_id, tipo_destino, destino_id, texto) 
        VALUES (?, ?, ?, ?)
    """, (remitente_id, tipo_destino, destino_id, texto))
    conn.commit()
    return cursor.lastrowid

def obtener_mensajes_canal(conn, canal_id):
    """Obtiene los mensajes de un canal incluyendo el username del remitente."""
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.*, u.username 
        FROM mensajes m
        JOIN usuarios u ON m.remitente_id = u.id
        WHERE m.tipo_destino = 'canal' AND m.destino_id = ?
        ORDER BY m.fecha_hora ASC
    """, (canal_id,))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def obtener_mensajes_privados(conn, usuario_a, usuario_b):
    """Obtiene el historial de chat privado entre dos usuarios específicos (en ambas direcciones)."""
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.*, u.username as username_remitente
        FROM mensajes m
        JOIN usuarios u ON m.remitente_id = u.id
        WHERE m.tipo_destino = 'privado' 
          AND ((m.remitente_id = ? AND m.destino_id = ?) OR (m.remitente_id = ? AND m.destino_id = ?))
        ORDER BY m.fecha_hora ASC
    """, (usuario_a, usuario_b, usuario_b, usuario_a))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]





