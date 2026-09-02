# test_app.py permitira correr las pruebas unitarias de la interfaz de la webapp usando pytest y flask.

# configurar entorno de pruebas
import pytest
import json
import sqlite3
import app as flask_app
import database

"""
@pytest.fixture
def cliente_web():
  

    flask_app.DB_FILE = ":memory:"  # usar una base de datos en memoria para pruebas

    # inicializar la DB temporal en memoria

    conn =sqlite3.connect(":memory:")
    database.inicializar_db(conn)
    conn.close()

    # Activar modo de prueba en Flask
    flask_app.app.config.update({"TESTING": True})

    # retornar el cliente web simulado
    with flask_app.app.test_client() as client:
        yield client

    

@pytest.fixture
def cliente_web():
    #Configura Flask para usar SQLite en memoria compartida y mantiene la BD viva.
    DB_PRUEBAS = "file:chatapp_test?mode=memory&cache=shared
    
    # 1. Pasamos la configuración a Flask
    flask_app.app.config["DB_FILE"] = DB_PRUEBAS
    flask_app.app.config["TESTING"] = True
    
    # 2. Abrimos la conexión "MAESTRA". Al no cerrarla aquí, 
    # garantizamos que la memoria RAM no se borre durante el test.
    conn_maestra = sqlite3.connect(DB_PRUEBAS, uri=True)
    database.inicializar_db(conn_maestra)
    
    # 3. Cedemos el cliente a los tests para que ejecuten las peticiones HTTP
    with flask_app.app.test_client() as client:
        yield client
     


    # 4. CUANDO EL TEST TERMINA, cerramos la conexión maestra.
    # Aquí es donde finalmente se limpia la memoria RAM de forma segura.
    conn_maestra.close()

"""

@pytest.fixture
def cliente_web(request):
    """Configura Flask para usar una base de datos en memoria única para CADA test."""
    # Usamos el nombre del test actual (request.node.name) para crear una base de datos única en RAM
    nombre_test = request.node.name
    DB_PRUEBAS = f"file:{nombre_test}?mode=memory&cache=shared"
    
    # 1. Pasamos la configuración única a Flask
    flask_app.app.config["DB_FILE"] = DB_PRUEBAS
    flask_app.app.config["TESTING"] = True
    
    # 2. Abrimos la conexión maestra para este test en específico
    conn_maestra = sqlite3.connect(DB_PRUEBAS, uri=True)
    database.inicializar_db(conn_maestra)
    
    # 3. Cedemos el cliente al test
    with flask_app.app.test_client() as client:
        yield client
        
    # 4. Al terminar el test, cerramos la conexión y la RAM de este test se destruye por completo
    conn_maestra.close()





# --- PRUEBA 1: POST (CREATE) ---
def test_api_crear_usuario_exitoso(cliente_web):
    # Datos simulados del perfil de chat
    datos_usuario = {
        "username": "lucas_chat",
        "nombre": "Lucas Silva",
        "biografia": "Probando la API con Pytest"
    }
    
    # Enviamos la petición POST simulando a Thunder Client
    respuesta = cliente_web.post("/usuarios", json=datos_usuario)
    
    # Verificaciones (Asserts)
    assert respuesta.status_code == 201
    assert respuesta.json["id"] == 1
    assert respuesta.json["mensaje"] == "Perfil creado con éxito"


# --- PRUEBA 2: GET (READ) ---
def test_api_obtener_usuario_no_encontrado(cliente_web):
    # Intentamos buscar un usuario que no existe en la base de datos limpia
    respuesta = cliente_web.get("/usuarios/99")
    
    assert respuesta.status_code == 404
    assert respuesta.json["error"] == "Usuario no encontrado"

# --- PRUEBA 3: PUT (UPDATE) y GET exitoso ---
def test_api_actualizar_perfil(cliente_web):
    # Primero creamos un usuario base
    cliente_web.post("/usuarios", json={"username": "marta", 
                                        "nombre": "Marta", 
                                        "biografia": "Hola"})
    
    # Modificamos los datos enviando un PUT al ID 1
    datos_nuevos = {"nombre": "Marta R.", 
                    "biografia": "Modo reunión"}
    respuesta_put = cliente_web.put("/usuarios/1", json=datos_nuevos)
    
    assert respuesta_put.status_code == 200
    assert respuesta_put.json["mensaje"] == "Perfil actualizado"
    
    # Validamos con un GET que los cambios se guardaron correctamente
    respuesta_get = cliente_web.get("/usuarios/1")
    assert respuesta_get.json["nombre"] == "Marta R."
    assert respuesta_get.json["biografia"] == "Modo reunión"


# --- PRUEBA 4: VALIDACIÓN DE USERNAME DUPLICADO (Debe devolver 400) ---
def test_api_crear_usuario_duplicado(cliente_web):
    usuario = {"username": "clara_chat", "nombre": "Clara", "biografia": "Hola"}
    
    # Registramos al usuario por primera vez (Éxito)
    primer_intento = cliente_web.post("/usuarios", json=usuario)
    assert primer_intento.status_code == 201
    
    # Intentamos registrar exactamente el mismo username (Debe fallar)
    segundo_intento = cliente_web.post("/usuarios", json=usuario)
    
    assert segundo_intento.status_code == 400
    assert segundo_intento.json["error"] == "El nombre de usuario ya existe"


# --- PRUEBA 5: VALIDACIÓN DE CAMPOS OBLIGATORIOS VACÍOS (Debe devolver 400) ---
def test_api_crear_usuario_campos_vacios(cliente_web):
    # Intentamos registrar un usuario sin el campo obligatorio 'nombre'
    usuario_invalido = {"username": "test_user", "biografia": "Sin nombre..."}
    
    respuesta = cliente_web.post("/usuarios", json=usuario_invalido)
    
    assert respuesta.status_code == 400
    assert respuesta.json["error"] == "Los campos username y nombre son obligatorios"

# --- PRUEBA 6: RUTA DE INICIO (HOME /) ---
def test_api_ruta_inicio(cliente_web):
    respuesta = cliente_web.get("/")
    
    assert respuesta.status_code == 200
    
    # as_text=True convierte los bytes a un string normal de Python
    texto_respuesta = respuesta.get_data(as_text=True)
    
    # Ahora puedes validar texto con caracteres especiales sin errores
    assert "¡Servidor de ChatApp funcionando correctamente!" in texto_respuesta



# --- PRUEBA 7: BORRAR USUARIO (DELETE) ---
def test_api_eliminar_usuario_exitoso(cliente_web):
    # 1. Primero creamos un usuario que vamos a borrar
    respuesta_post = cliente_web.post(
        "/usuarios", 
        json={"username": "borrame_chat", "nombre": "Usuario Temporal", "biografia": "Adiós"}
    )
    user_id = respuesta_post.json["id"]
    
    # 2. Enviamos la petición DELETE usando el ID generado
    respuesta_delete = cliente_web.delete(f"/usuarios/{user_id}")
    
    assert respuesta_delete.status_code == 200
    assert respuesta_delete.json["mensaje"] == "Perfil eliminado"
    
    # 3. Validamos con un GET que el usuario realmente ya no exista (404)
    respuesta_get = cliente_web.get(f"/usuarios/{user_id}")
    assert respuesta_get.status_code == 404


# --- PRUEBA 8: TEXTO VACÍO CON ESPACIOS (Para llegar al 100% de cobertura) ---
def test_api_crear_usuario_con_espacios_blancos(cliente_web):
    # Enviamos campos que existen, pero están llenos de espacios en blanco
    usuario_invalido = {
        "username": "   ", 
        "nombre": "Andrés", 
        "biografia": "Probando espacios"
    }
    
    respuesta = cliente_web.post("/usuarios", json=usuario_invalido)
    
    assert respuesta.status_code == 400
    assert respuesta.json["error"] == "Los campos username y nombre son obligatorios"




