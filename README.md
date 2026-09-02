# README
"""
En la metodología TDD, una vez que la lógica  (las funciones matemáticas) está limpia, refactorizada y protegida por pruebas, el siguiente paso es separar la interfaz de usuario (la entrada por teclado) de la lógica pura.
En TDD, nunca se ponen inputs de teclado (input()) dentro de las funciones que tienen las pruebas, porque las pruebas se ejecutan automáticamente y no pueden "escribir" en la terminal.

Separación de Responsabilidades (SRP): el archivo calculadora.py solo sabe 
procesar datos (lógica pura). 

Tu archivo main.py solo sabe hablar con el usuario (interfaz).

Automatización: 
Se puedes cambiar main.py para que en lugar del teclado lea los números de 
un archivo web o una base de datos, y tus pruebas 
en calculadora.py seguirán funcionando intactas sin cambiar una sola línea.
"""

"""
pip install flask pytest pytest-cov


Ahora estoy probando la metodologia TDD en desarrollo WEB con Flask, y una sqlite3. Los archivos correspondientes
a estas pruebas son 
app.py
database.py
test_app.py
test_database.py
