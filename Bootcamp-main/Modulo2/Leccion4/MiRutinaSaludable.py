# --- DEFINICIÓN DE FUNCIONES (MÓDULOS) ---
def calcular_imc(peso, altura):
    """Calcula el IMC usando la fórmula: peso / altura^2."""
    return peso / (altura ** 2)

def clasificar_imc(imc):
    """Clasifica el resultado del IMC en categorías de salud."""
    if imc < 18.5:
        return "Bajo peso"
    elif 18.5 <= imc <= 24.9:
        return "Normal"
    elif 25 <= imc <= 29.9:
        return "Sobrepeso"
    else:
        return "Obesidad"

# --- LÓGICA PRINCIPAL (EJECUCIÓN) ---

def ejecutar_sistema():

    # 2. Parte del IMC
    print("--- Calculadora de IMC ---")
    peso = float(input("Ingresa tu peso en kg: "))
    altura = float(input("Ingresa tu altura en metros: "))
    
    valor_imc = calcular_imc(peso, altura)
    categoria = clasificar_imc(valor_imc)
    
    print(f"Tu IMC es {round(valor_imc, 2)} y tu categoría es: {categoria}")

if __name__ == "__main__":
    ejecutar_sistema()