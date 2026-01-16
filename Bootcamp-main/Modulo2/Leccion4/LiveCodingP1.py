def calcular_imc(peso, altura):
    """Calcula el IMC usando la fórmula: peso / altura al cuadrado."""
    return peso / (altura ** 2)

def clasificar_imc(imc):
    """Devuelve la categoría de salud basada en el valor del IMC."""
    if imc < 18.5:
        return "Bajo peso"
    elif 18.5 <= imc < 25:
        return "Peso normal"
    elif 25 <= imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"

def ejecutar_programa():
    """Función principal que coordina la entrada, el cálculo y la salida."""
    print("--- Calculadora de IMC ---")
    
    # Uso de input() y conversión a float()
    try:
        peso = float(input("Ingresa tu peso en kg (ej. 75): "))
        altura = float(input("Ingresa tu altura en metros (ej. 1.75): "))

        # Cálculo y clasificación
        valor_imc = calcular_imc(peso, altura)
        categoria = clasificar_imc(valor_imc)

        # Mostrar resultado con print()
        print(f"\nTu IMC es: {valor_imc:.2f}")
        print(f"Clasificación: {categoria}")
        
    except ValueError:
        print("Error: Por favor ingresa solo números usando el punto para decimales.")

# Separar código principal del resto
if __name__ == "__main__":
    ejecutar_programa()

"""El "Interruptor" de Seguridad 🚦
La línea if __name__ == "__main__": actúa como un filtro. Dice: "Solo si el usuario abrió este archivo para ejecutarlo, entonces inicia la función ejecutar_programa()".

Si no pusiéramos este if, al intentar usar solo una función de este archivo en un proyecto nuevo (usando import), 
Python ejecutaría automáticamente todo el programa (pediría el peso, la altura, etc.), lo cual suele ser molesto y desordenado.

Al usar este "interruptor", podemos importar funciones desde este archivo sin que se ejecute el programa completo, manteniendo todo ordenado y bajo control."""