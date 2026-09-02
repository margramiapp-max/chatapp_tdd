# usando la tecnica de programacion TDD Test Driven Development, en donde se escriben primero las pruebas unitarias antes de escribir el código funcional. 
# Esto asegura que el código cumpla con los requisitos especificados y facilita la detección de errores desde el principio del desarrollo.
# Primero exploraré la técnica y luego aplicare agentic AI para mirar si mejora el proceso de generacion de codigo.
# primero con unittest y luego con pytest
# OJO con pytest es critico el nombre de las funciones de prueba, deben empezar con test_ para que pytest las reconozca como pruebas unitarias.
# tambien el nombre del archivo de prueba debe empezar con test_ para que pytest lo reconozca como un archivo de prueba unitaria.


"""import unittest
from calculadora import sumar_positivos, multiplicar_positivos

class TestCalculadora(unittest.TestCase):
    def test_sumar_positivos(self):
        self.assertEqual(sumar_positivos([5, -2, 3, -1, 0]), 8)

    def test_multiplicar_positivos(self):
        self.assertEqual(multiplicar_positivos([1, -2, -3, 4, 5]), 20)



if __name__ == '__main__':
    unittest.main()
"""


# con pytest
"""from calculadora import sumar_positivos, multiplicar_positivos

def test_sumar_positivos(): 
    assert sumar_positivos([5, -2, 3, -1, 0]) == 8

def test_multiplicar_positivos():    
    assert multiplicar_positivos([1, -2, -3, 4, 5]) == 20
    """

import pytest
from calculadora import multiplicar_positivos, sumar_positivos

# Definimos múltiples escenarios: (entrada, resultado_esperado)
@pytest.mark.parametrize("lista_entrada, resultado_esperado", [
    ([2, -5, 3, 0, 4], 24), # Caso base
    ([], 0),                # Caso: Lista vacía
    ([-1, -2, -3], 0),      # Caso: Solo números negativos
])
def test_multiplicar_varios_escenarios(lista_entrada, resultado_esperado):
    assert multiplicar_positivos(lista_entrada) == resultado_esperado

def test_sumar_positivos(): 
    assert sumar_positivos([5, -2, 3, -1, 0]) == 8





