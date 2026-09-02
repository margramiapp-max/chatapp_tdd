# database.py implementa la estructura inicial de la base de datos y las funciones para interactuar con ella.

import sqlite3

def inicializar_db(conn):
    """Crea la tabla de perfiles de usuario si no existe."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            biografia TEXT
        )
    """)
    conn.commit()

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



