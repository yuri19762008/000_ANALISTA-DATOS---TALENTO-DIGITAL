def calcular_imc(peso,altura):
    """Calcula el Índice de Masa Corporal (IMC) dado el peso en kg y la altura en metros."""
    return peso / (altura ** 2)

def clasificar_imc(imc):
    """Devuelve la categoria de salud basada en el valor del IMC."""
    if imc < 18.5:
        return "Bajo peso"
    elif 18.5 <= imc < 24.9:
        return "Peso normal"
    elif 25 <= imc < 29.9:
        return "Sobrepeso"
    else:
        return "Obesidad"


def ejecutar_programa():
    peso = float(input("Ingrese su peso en kg: (ej. 75) "))
    altura = float(input("Ingrese su altura en metros: (ej. 1.75) "))

    imc = calcular_imc(peso, altura)
    categoria = clasificar_imc(imc)

    print("Su IMC es: {:.2f}".format(imc))
    print("Categoría de salud:", categoria)

# Separar código principal del resto
if __name__ == "__main__":
   ejecutar_programa()


