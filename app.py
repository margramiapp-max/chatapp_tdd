# app.py es la interfaz que llama a las funciones en database.py. Las respuestas que se envían al cliente son en formato JSON, 


from flask import Flask, request, jsonify, render_template
import sqlite3
import database

app = Flask(__name__)
DB_FILE = "chatapp.db"



def obtener_conexion():
    # En lugar de usar la variable global fija, usamos la configuración de la app de Flask
    # Si app.config['DB_FILE'] no existe, por defecto usa "chatapp.db"
    db_actual = app.config.get("DB_FILE", "chatapp.db")
    
    conn = sqlite3.connect(db_actual, uri=True)  # uri=True permite usar URIs como "file:chatapp_test?mode=memory&cache=shared" sin escribir en el disco
    database.inicializar_db(conn)
    return conn

@app.route("/", methods=["GET"])
def inicio():
    return "¡Servidor de ChatApp funcionando correctamente!"



@app.route("/usuarios", methods=["POST"])
def api_crear_usuario():
    datos = request.json
    
    # VALIDACIÓN: Verificar que los campos obligatorios existan
    if not datos or "username" not in datos or "nombre" not in datos:
        return jsonify({"error": "Los campos username y nombre son obligatorios"}), 400
        
    # Validar que no sean textos vacíos
    if not str(datos["username"]).strip() or not str(datos["nombre"]).strip():
        return jsonify({"error": "Los campos username y nombre son obligatorios"}), 400

    conn = obtener_conexion()
    try:
        user_id = database.crear_usuario(conn, datos["username"], datos["nombre"], datos.get("biografia", ""))
        return jsonify({"id": user_id, "mensaje": "Perfil creado con éxito"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El nombre de usuario ya existe"}), 400
    finally:
        conn.close()


@app.route("/usuarios/<int:user_id>", methods=["GET"])
def api_obtener_usuario(user_id):
    conn = obtener_conexion()
    usuario = database.obtener_usuario(conn, user_id)
    conn.close()
    if usuario:
        return jsonify(usuario), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route("/usuarios/<int:user_id>", methods=["PUT"])
def api_actualizar_usuario(user_id):
    datos = request.json
    conn = obtener_conexion()
    database.actualizar_usuario(conn, user_id, datos["nombre"], datos["biografia"])
    conn.close()
    return jsonify({"mensaje": "Perfil actualizado"}), 200

@app.route("/usuarios/<int:user_id>", methods=["DELETE"])
def api_eliminar_usuario(user_id):
    conn = obtener_conexion()
    database.eliminar_usuario(conn, user_id)
    conn.close()
    return jsonify({"mensaje": "Perfil eliminado"}), 200




if __name__ == "__main__":
    app.run(debug=True)

