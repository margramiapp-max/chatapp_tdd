# app.py es la interfaz que llama a las funciones en database.py


from flask import Flask, request, render_template, redirect, url_for

import sqlite3
import database

app = Flask(__name__)
DB_FILE = "chatapp.db"

def obtener_conexion():
    db_actual = app.config.get("DB_FILE", "chatapp.db")
    # check_same_thread=False evita bloqueos concurrentes en el navegador
    conn = sqlite3.connect(db_actual, uri=True, check_same_thread=False)
    database.inicializar_db(conn)
    return conn

# --- RUTA PRINCIPAL CON JINJA2 ---
@app.route("/", methods=["GET", "POST"])
def inicio():
    conn = obtener_conexion()
    
    # Si el usuario envía el formulario de login/registro
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        nombre = request.form.get("nombre", "").strip()
        
        if username and nombre:
            try:
                # Intentamos crear el usuario (si ya existe, saltará a la excepción)
                database.crear_usuario(conn, username, nombre, "¡Usando ChatApp!")
            except sqlite3.IntegrityError:
                pass # Si ya existe, simplemente lo dejamos pasar para iniciar sesión
            
            # Buscamos el ID del usuario para mantener la sesión en la URL
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
            user_row = cursor.fetchone()
            
            if user_row:
                conn.close()
                return redirect(f"/?user_id={user_row['id']}")

    # Lógica para mostrar la pantalla de chat si ya está logueado
    user_id = request.args.get("user_id")
    usuario_actual = None
    usuarios = []
    mensajes = []

    if user_id:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 1. Obtener datos del usuario actual
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            usuario_actual = dict(row)
            
            # 2. Listar el resto de usuarios
            cursor.execute("SELECT id, username, nombre FROM usuarios WHERE id != ?", (user_id,))
            usuarios = [dict(r) for r in cursor.fetchall()]
            
            # 3. Obtener los mensajes del Canal General (ID 1) por defecto
            mensajes = database.obtener_mensajes_canal(conn, 1)

    conn.close()
    return render_template("index.html", 
                           usuario_actual=usuario_actual, 
                           usuarios=usuarios, 
                           mensajes=mensajes)

# --- RUTA PARA ENVIAR MENSAJES VIA FORMULARIO JINJA2 ---
@app.route("/enviar_mensaje", methods=["POST"])
def api_enviar_mensaje():
    remitente_id = request.form.get("remitente_id")
    texto = request.form.get("texto", "").strip()
    
    if remitente_id and texto:
        conn = obtener_conexion()
        # Por ahora enviamos todo al canal general (tipo_destino="canal", destino_id=1)
        database.enviar_mensaje(conn, int(remitente_id), "canal", 1, texto)
        conn.close()
        
    return redirect(f"/?user_id={remitente_id}")

if __name__ == "__main__":
    app.run(debug=True)

