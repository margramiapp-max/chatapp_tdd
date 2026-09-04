# Test_database.py  Este archivo contiene los text que correra pytest y usa una base de datos en memoria para probar 
# las funciones CRUD de database.py. Ya que las pruebas necesitan velocidad y aislamiento.



import pytest
import sqlite3

from database import inicializar_db, crear_usuario, obtener_usuario, actualizar_usuario, eliminar_usuario

@pytest.fixture
def db_conn():
    """Configura una  base de datos limpia en memoria para cada prueba."""
    conn = sqlite3.connect(':memory:')
    inicializar_db(conn)
    return conn

# Prueba 1: CREATE (Fallará inicialmente porque database.py esta vacio)
def test_crear_y_obtener_usuario(db_conn):
    # Intentamos registrar un perfil de chat
    user_id = crear_usuario(db_conn, "juan_chat", "Juan Pérez", "¡Hola! Estoy usando ChatApp.")
    
    # Intentamos leerlo (READ)
    usuario = obtener_usuario(db_conn, user_id)
    
    assert usuario is not None
    assert usuario["username"] == "juan_chat"
    assert usuario["nombre"] == "Juan Pérez"
    assert usuario["biografia"] == "¡Hola! Estoy usando ChatApp." 



# PRUEBA2 : Posting messages

from database import enviar_mensaje, obtener_mensajes_canal, obtener_mensajes_privados

def test_enviar_y_leer_mensaje_canal_general(db_conn):
    # 1. Creamos el usuario que envía
    remitente_id = crear_usuario(db_conn, "carlos_dev", "Carlos", "Bio")
    
    # 2. Envia un mensaje al canal general (tipo_destino="canal", destino_id=1)
    msg_id = enviar_mensaje(db_conn, remitente_id, "canal", 1, "¡Hola a todos en el canal general!")
    assert msg_id is not None
    
    # 3. Leemos los mensajes del canal general
    mensajes_canal = obtener_mensajes_canal(db_conn, 1)
    assert len(mensajes_canal) == 1
    assert mensajes_canal[0]["texto"] == "¡Hola a todos en el canal general!"
    assert mensajes_canal[0]["username"] == "carlos_dev"  # ¡Queremos saber quién lo envió!

def test_enviar_y_leer_mensajes_privados_one_to_one(db_conn):
    # 1. Creamos dos usuarios (Juan y Ana)
    juan_id = crear_usuario(db_conn, "juan99", "Juan", "Bio")
    ana_id = crear_usuario(db_conn, "ana_g", "Ana", "Bio")
    
    # 2. Juan le envía un mensaje privado a Ana (tipo_destino="privado", destino_id=ana_id)
    enviar_mensaje(db_conn, juan_id, "privado", ana_id, "Hola Ana, ¿cómo estás?")
    # Ana le responde a Juan
    enviar_mensaje(db_conn, ana_id, "privado", juan_id, "Hola Juan! Todo bien.")
    
    # 3. Consultamos el historial del chat privado entre Juan y Ana
    chat_historial = obtener_mensajes_privados(db_conn, juan_id, ana_id)
    
    assert len(chat_historial) == 2
    assert chat_historial[0]["texto"] == "Hola Ana, ¿cómo estás?"
    assert chat_historial[0]["remitente_id"] == juan_id
    assert chat_historial[1]["texto"] == "Hola Juan! Todo bien."
