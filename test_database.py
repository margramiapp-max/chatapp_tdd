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