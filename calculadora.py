# calculadora
import math

def sumar_positivos(numeros):
   
    return sum(num for num in numeros if num > 0)


# NUEVA FUNCIÓN (Código mínimo para ganar el "Verde")
"""def multiplicar_positivos(numeros):
    positivos = [num for num in numeros if num > 0]
    
    if not positivos:
        return 0
        
    resultado = 1
    for num in positivos:
        resultado *= num
    return resultado"""

def multiplicar_positivos(numeros):
    positivos = [num for num in numeros if num > 0]
    return math.prod(positivos) if positivos else 0
