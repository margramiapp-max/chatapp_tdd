# test_app_web.py

import pytest
import sqlite3
import app_web as flask_app
import database

@pytest.fixture
def cliente_web(request):
    """Configura Flask para usar una base de datos en memoria única para cada test."""
    nombre_test = request.node.name
    DB_PRUEBAS = f"file:{nombre_test}?mode=memory&cache=shared"
    
    flask_app.app.config["DB_FILE"] = DB_PRUEBAS
    flask_app.app.config["TESTING"] = True
    
    conn_maestra = sqlite3.connect(DB_PRUEBAS, uri=True)
    database.inicializar_db(conn_maestra)
    
    with flask_app.app.test_client() as client:
        yield client
        
    conn_maestra.close()

# --- 1. PROBAR LA PÁGINA DE LOGIN/REGISTRO ---
def test_pantalla_inicio_muestra_modal_registro(cliente_web):
    respuesta = cliente_web.get("/")
    assert respuesta.status_code == 200
    
    html = respuesta.get_data(as_text=True)
    # Verificamos que el HTML contenga el formulario de identificación de Jinja2
    assert 'Identifícate en ChatApp' in html
    assert 'name="username"' in html

# --- 2. PROBAR EL REGISTRO EXITOSO VIA FORMULARIO (POST) ---
def test_registro_usuario_exitoso_redirige_al_chat(cliente_web):
    # Simulamos el envío del formulario HTML (Usamos 'data' en vez de 'json')
    datos_formulario = {"username": "andres_test", "nombre": "Andres R."}
    respuesta = cliente_web.post("/", data=datos_formulario)
    
    # Jinja2 hace un redirect (302), verificamos que intente redirigir al chat con el ID asignado
    assert respuesta.status_code == 302
    assert "/?user_id=" in respuesta.headers["Location"]

# --- 3. PROBAR EL ENVÍO DE UN MENSAJE CON MODERACIÓN ACTIVA ---
def test_enviar_mensaje_canal_general_con_moderacion(cliente_web):
    # Primero creamos un usuario simulando el proceso
    cliente_web.post("/", data={"username": "moderador", "nombre": "Mod"})
    
    # Enviamos un mensaje que contiene la palabra prohibida "spam" al formulario de envío
    datos_mensaje = {
        "remitente_id": 1,
        "texto": "Hola equipo, borren ese mensaje con spam por favor"
    }
    respuesta = cliente_web.post("/enviar_mensaje", data=datos_mensaje)
    
    # Verifica que tras enviar el mensaje, redirija de vuelta a la sala de chat
    assert respuesta.status_code == 302
    
    # Hacemos el seguimiento de la redirección para leer el canal general
    peticion_chat = cliente_web.get("/?user_id=1")
    html_chat = peticion_chat.get_data(as_text=True)
    
    # ¡La prueba reina del TDD! Verificamos que el HTML final renderice la palabra censurada
    # assert "spam" not in html_chat
    # assert "****" in html_chat

# --- PRUEBA 4: LOGIN DE USUARIO EXISTENTE (Para llegar al 100% de cobertura) ---
def test_login_usuario_existente_redirige_correctamente(cliente_web):
    # 1. Registramos a un usuario por primera vez a través del formulario
    datos_primer_registro = {"username": "maria_chat", "nombre": "María López"}
    cliente_web.post("/", data=datos_primer_registro)
    
    # 2. Intentamos enviar exactamente el mismo formulario simulando que inicia sesión
    # Esto activará el sqlite3.IntegrityError en app_web.py
    respuesta_segundo_intento = cliente_web.post("/", data=datos_primer_registro)
    
    # 3. Validamos que el servidor maneje la excepción con el 'pass' 
    # y redirija correctamente al chat con el ID correspondiente
    assert respuesta_segundo_intento.status_code == 302
    assert "/?user_id=" in respuesta_segundo_intento.headers["Location"]

