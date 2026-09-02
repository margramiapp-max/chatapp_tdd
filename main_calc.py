# Crear interfaz de usuario

from calculadora import sumar_positivos, multiplicar_positivos

def solicitar_numeros():
    print("--- Calculadora de Positivos ---")
    entrada = input("Introduce números enteros separados por espacios (ej: 2 -5 3 0 4): ")
    
    # Convertimos el texto ingresado en una lista de números enteros
    try:
        numeros = [int(x) for x in entrada.split()]
        return numeros
    except ValueError:
        print("Error: Por favor, introduce solo números válidos.")
        return None

def ejecutar_programa():
    numeros = solicitar_numeros()
    
    if numeros is not None:
        suma = sumar_positivos(numeros)
        multiplicacion = multiplicar_positivos(numeros)
        
        print("\n--- Resultados ---")
        print(f"Lista procesada: {numeros}")
        print(f"Suma de positivos: {suma}")
        print(f"Multiplicación de positivos: {multiplicacion}")

if __name__ == "__main__":
    ejecutar_programa()
